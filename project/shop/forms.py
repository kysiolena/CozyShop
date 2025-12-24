from django import forms


class BootstrapFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop through all fields and add Bootstrap classes
        for field_name, field in self.fields.items():
            # Add form-control class to the input element
            field.widget.attrs.update({"class": "form-control"})

            # Check for checkboxes (if any) as they need a different class in Bootstrap
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})

            # Check if the form is bound and if the field has errors
            if self.is_bound and self.errors.get(field_name):
                # Get existing classes or initialize an empty list
                existing_classes = field.widget.attrs.get("class", "").split()
                # Add 'is-invalid' if it's not already there
                if "is-invalid" not in existing_classes:
                    existing_classes.append("is-invalid")
                # Update the 'class' attribute
                field.widget.attrs.update({"class": " ".join(existing_classes)})
