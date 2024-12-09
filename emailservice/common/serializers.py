from rest_framework import serializers

class CustomModelSerializer(serializers.ModelSerializer):
    """
    A custom ModelSerializer that extends the default functionality.
    """

    def create(self, validated_data):
        """
        Create a new instance of the model.
        """
        # Custom logic before creation
        instance = super().create(validated_data)
        # Custom logic after creation
        return instance

    def update(self, instance, validated_data):
        """
        Update an existing instance of the model.
        """
        instance = super().update(instance, validated_data)
        # Custom logic after update
        return instance

    def save(self, **kwargs):
        """
        Save the instance, handling both creation and update.
        """
        # Custom logic before save
        if self.instance is None:
            # This is a creation
            self.instance = self.create(self.validated_data)
        else:
            # This is an update
            self.instance = self.update(self.instance, self.validated_data)

        # Custom logic after save
        return self.instance

    def delete(self, instance):
        """
        Delete the instance.
        """
        # Custom logic before delete
        instance.deletes()
        # Custom logic after delete

    def to_representation(self, instance):
        """
        Convert the instance to a dictionary of primitive data types.
        """
        # Custom logic before representation
        representation = super().to_representation(instance)
        # Custom logic after representation
        return representation

    def to_internal_value(self, data):
        """
        Convert the input data to a validated dictionary of native values.
        """
        # Custom logic before internal value conversion
        internal_value = super().to_internal_value(data)
        # Custom logic after internal value conversion
        return internal_value