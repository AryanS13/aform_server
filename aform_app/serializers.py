from rest_framework import serializers
from .models import Form, Field, FieldProperty, Logic, Actions, Condition, ConditionVariable

class ConditionVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConditionVariable
        fields = '__all__'

class ConditionSerializer(serializers.ModelSerializer):
    vars = ConditionVariableSerializer(many=True, required=False)

    class Meta:
        model = Condition
        fields = '__all__'

    def create(self, validated_data):
        vars_data = validated_data.pop('vars', [])
        condition = Condition.objects.create(**validated_data)
        for var_data in vars_data:
            ConditionVariable.objects.create(condition=condition, **var_data)
        return condition

class ActionSerializer(serializers.ModelSerializer):
    condition = ConditionSerializer()

    class Meta:
        model = Actions
        fields = '__all__'

    def create(self, validated_data):
        condition_data = validated_data.pop('condition')
        condition = ConditionSerializer.create(ConditionSerializer(), validated_data=condition_data)
        action = Actions.objects.create(condition=condition, **validated_data)
        return action

class LogicSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(many=True)

    class Meta:
        model = Logic
        fields = '__all__'

    def create(self, **validated_data):
        validated_data = validated_data.pop('validated_data', None)
        actions_data = validated_data.pop('actions', None)
        logic = Logic.objects.create(**validated_data)
        for action_data in actions_data:
            action_data['logic'] = logic
            ActionSerializer.create(ActionSerializer(), validated_data=action_data)
        return logic

class FieldPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldProperty
        fields = '__all__'

class FieldSerializer(serializers.ModelSerializer):
    properties = FieldPropertySerializer()

    class Meta:
        model = Field
        fields = '__all__'

    def create(self, validated_data):
        properties_data = validated_data.pop('properties')
        field_property = FieldProperty.objects.create(**properties_data)
        field = Field.objects.create(properties=field_property, **validated_data)
        return field

class FormSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)
    logic = LogicSerializer(many=True)

    class Meta:
        model = Form
        fields = '__all__'

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        logic_data = validated_data.pop('logic')

        for logic in logic_data:
            print('Pre rendered')
            print(logic)
        form = Form.objects.create(**validated_data)
        for field_data in fields_data:
            field_data['form'] = form
            FieldSerializer.create(FieldSerializer(), validated_data=field_data)
        for logic_data_item in logic_data:
            logic_data_item['form'] = form
            print(logic_data_item)
            print('logic')
            LogicSerializer.create(LogicSerializer(), validated_data=logic_data_item)
        return form
