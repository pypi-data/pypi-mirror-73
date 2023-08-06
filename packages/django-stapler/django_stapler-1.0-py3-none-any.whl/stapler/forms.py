from django.forms.forms import BaseForm
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms.forms import DeclarativeFieldsMetaclass
from django.forms.models import construct_instance, model_to_dict, InlineForeignKeyField
from itertools import chain


def prepend_prefix(cls, data):
    d = {}
    prefix = f'{cls.__name__.lower()}'
    for k, v in data.items():
        d[f'{prefix}__{k}'] = v
    return d

def strip_prefix(cls, data):
    d = {}
    prefix = f'{cls.__name__.lower()}__'
    for k, v in data.items():
        if prefix in k:
            _, nk = k.split(prefix)
            d[nk] = v
    return d


class StaplerFormOptions:

    def __init__(self, options):
        self.modelforms = getattr(options, 'modelforms')


class StaplerMetaclass(DeclarativeFieldsMetaclass):

    def __new__(mcs, name, bases, attrs):

        # gather the fields of the inner Meta class and add them to attrs
        meta = attrs.pop('Meta', None)
        if meta:
            if not hasattr(meta, 'modelforms'):
                raise AttributeError('make sure that modelforms attribute is set in inner Meta class')
            for form in meta.modelforms:
                # add class name prefix to fieldnames to prevent clashing between model fields
                base_fields = prepend_prefix(form._meta.model, form.base_fields)
                attrs.update(base_fields)

            # add options from meta class
            attrs['_meta'] = StaplerFormOptions(meta)
        else:
            pass #raise TypeError('StaplerForm is missing class Meta.')

        return super().__new__(mcs, name, bases, attrs)


class StaplerBaseForm(BaseForm):

    def __init__(self, **kwargs):

        instances = kwargs.pop('instances', [])
        initial = kwargs.get('initial')
        ac_object_data = {}

        # get all ModelForms
        for mf in self._meta.modelforms:
            opts = mf._meta
            mc = opts.model
            instance = self._get_instance(mc, instances)

            if instance is None:
                # if we didn't get an instance, instantiate a new one
                current_instance = mc()
                object_data = {}
            else:
                current_instance = instance
                object_data = model_to_dict(instance, opts.fields, opts.exclude)

            ac_object_data.update(prepend_prefix(mc, object_data))

            # set attribute for instance
            setattr(self, f'{mc.__name__.lower()}_instance', current_instance)

        # if initial was provided, it should override the values from instance
        if initial is not None:
            ac_object_data.update(initial)

        kwargs['initial'] = ac_object_data
        super().__init__(**kwargs)

    def _get_instance(self, mc, instances):
        for instance in instances:
            if type(instance) == mc:
                return instance

    def _get_instances(self):
        mcs = [m._meta.model.__name__.lower() for m in self._meta.modelforms]
        attr_names = [f'{m}_instance' for m in mcs]
        instances = [getattr(self, attr_name) for attr_name in attr_names]
        return instances

    def _mc_to_mfc(self, mc):
        mfcs = self._meta.modelforms
        for mfc in mfcs:
            if mfc._meta.model == mc:
                return mfc

    def _get_validation_exclusions(self, mfc, mc):
        """
        For backwards-compatibility, exclude several types of fields from model
        validation. See tickets #12507, #12521, #12553.
        """
        exclude = []
        # Build up a list of fields that should be excluded from model field
        # validation and unique checks.
        for f in mc._meta.fields:  # self.instance._meta.fields:
            field = f.name

            # Exclude fields that aren't on the form. The developer may be
            # adding these values to the model after form validation.
            if field not in self.fields:
                exclude.append(f.name)

            # Don't perform model validation on fields that were defined
            # manually on the form and excluded via the ModelForm's Meta
            # class. See #12901.
            elif mfc._meta.fields and field not in mfc._meta.fields:
                exclude.append(f.name)

            elif mfc._meta.exclude and field in self._meta.exclude:
                exclude.append(f.name)

            # Exclude fields that failed form validation. There's no need for
            # the model fields to validate them as well.
            elif field in self._errors:
                exclude.append(f.name)

            # Exclude empty fields that are not required by the form, if the
            # underlying model field is required. This keeps the model field
            # from raising a required error. Note: don't exclude the field from
            # validation if the model field allows blanks. If it does, the blank
            # value may be included in a unique check, so cannot be excluded
            # from validation.
            else:
                form_field = self.fields[field]
                field_value = self.cleaned_data.get(field)
                if not f.blank and not form_field.required and field_value in form_field.empty_values:
                    exclude.append(f.name)
        return exclude

    def _post_clean(self):

        opts = self._meta
        mfcs = opts.modelforms

        # keep original cleaned data, required for workaround so we can keep using the construct_instance() function
        _cleaned_data = self.cleaned_data
        _fields = self.fields

        for mfc in mfcs:
            mc = mfc._meta.model
            current_instance = getattr(self, f'{mc.__name__.lower()}_instance')
            exclude = self._get_validation_exclusions(mfc, mc)

            # modify the cleaned data, it should only contain cleaned data for the current modelclass (mc)
            # in addition, the prefix should be removed so that the construct_instance function can be used
            # do so for fields attr to
            self.cleaned_data = strip_prefix(mc, _cleaned_data)
            self.fields = strip_prefix(mc,  _fields)

            # Foreign Keys being used to represent inline relationships
            # are excluded from basic field value validation. This is for two
            # reasons: firstly, the value may not be supplied (#12507; the
            # case of providing new values to the admin); secondly the
            # object being referred to may not yet fully exist (#12749).
            # However, these fields *must* be included in uniqueness checks,
            # so this can't be part of _get_validation_exclusions().
            #
            # create a instance to get acces to the fields attr
            #
            mfc_instance = mfc()
            for name, field in mfc_instance.fields.items():
                if isinstance(field, InlineForeignKeyField):
                    exclude.append(name)

            try:
                exclude_f = mfc._meta.exclude
            except AttributeError:
                exclude = None

            try:
                current_instance = construct_instance(self, current_instance, self.fields, exclude_f)
                setattr(self, f'{mc.__name__.lower()}_instance', current_instance)
            except ValidationError as e:
                self._update_errors(e)

            try:
                current_instance.full_clean(exclude=exclude, validate_unique=False)
            except ValidationError as e:
                self._update_errors(e)

            # Validate uniqueness if needed.
            if mfc_instance._validate_unique:
                self.validate_unique(mc, self._get_validation_exclusions(mfc, mc))

        # restore cleaned data
        self.cleaned_data = _cleaned_data
        self.fields = _fields

    def validate_unique(self, mc, exclude):
        """
        Call the instance's validate_unique() method and update the form's
        validation errors if any were raised.
        """
        instance = getattr(f'{mc.__name__.lower()}_instance')
        try:
            instance.validate_unique(exclude=exclude)
        except ValidationError as e:
            self._update_errors(e)

    def _update_errors(self, errors):
        # Override any validation error messages defined at the model level
        # with those defined at the form level.
        opts = self._meta

        # Allow the model generated by construct_instance() to raise
        # ValidationError and have them handled in the same way as others.
        if hasattr(errors, 'error_dict'):
            error_dict = errors.error_dict
        else:
            error_dict = {NON_FIELD_ERRORS: errors}

        for field, messages in error_dict.items():
            if (field == NON_FIELD_ERRORS and opts.error_messages and
                    NON_FIELD_ERRORS in opts.error_messages):
                error_messages = opts.error_messages[NON_FIELD_ERRORS]
            elif field in self.fields:
                error_messages = self.fields[field].error_messages
            else:
                continue

            for message in messages:
                if (isinstance(message, ValidationError) and
                        message.code in error_messages):
                    message.message = error_messages[message.code]

        self.add_error(None, errors)

    def _save_m2m(self):
        """
        Save the many-to-many fields and generic relations for this form.
        """
        instances = self._get_instances()
        for instance in instances:
            mfc = self._mc_to_mfc(type(instance))
            cleaned_data = self.cleaned_data
            exclude = mfc._meta.exclude
            fields = self.fields
            opts = instance._meta

            # Note that for historical reasons we want to include also
            # private_fields here. (GenericRelation was previously a fake
            # m2m field).
            for f in chain(opts.many_to_many, opts.private_fields):
                if not hasattr(f, 'save_form_data'):
                    continue
                if fields and f.name not in fields:
                    continue
                if exclude and f.name in exclude:
                    continue
                if f.name in cleaned_data:
                    f.save_form_data(instance, cleaned_data[f.name])

    def _save(self, commit=True):
        """
        Save this form's self.instance object if commit=True. Otherwise, add
        a save_m2m() method to the form which can be called after the instance
        is saved manually at a later time. Return the model instance.
        """
        if self.errors:
            raise ValueError(
                "At least one of the instances could not be created/changed because the data didn't validate.")

        instances = self._get_instances()
        if commit:
            # If committing, save the instance and the m2m data immediately.
            for instance in instances:
                instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        result = {f'{type(instance).__name__.lower()}_instance': instance for instance in instances}
        return result

    def pre_save(self):
        pass

    def post_save(self):
        pass

    def save(self):
        self.pre_save()
        instances = self._save()
        self.post_save()
        return instances


class StaplerForm(StaplerBaseForm, metaclass=StaplerMetaclass):
    pass


