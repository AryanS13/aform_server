from rest_framework import serializers
from .models import Form, Field, FieldProperty, Logic, Actions, Condition
            
class ConditionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # vars 

    class Meta:
        model = Condition
        fields = ('id', 'operator', 'order', 'type', 'value', 'vars', )
    
    def get_fields(self):
        fields = super(ConditionSerializer, self).get_fields()
        fields['vars'] = ConditionSerializer(many=True, required=False, allow_null=True)
        return fields

    # def create(self, validated_data):
    #     vars_data = validated_data.pop('vars', [])
    #     condition = Condition.objects.create(**validated_data)

    #     condition_vars = []
    #     for var_data in vars_data:
    #         var_instance = ConditionSerializer().create(var_data)
    #         var_instance.parent = condition
    #         var_instance.save()
    #         condition_vars.append(var_instance)

    #     condition.vars.set(condition_vars)
    #     return condition
    
    def create(self, validated_data):
        vars_data = validated_data.pop('vars', [])
        condition = Condition.objects.create(**validated_data)
        self._create_or_update_vars(condition, vars_data)
        return condition
    
    def update(self, instance, validated_data):
        vars_data = validated_data.pop('vars', [])
        instance.operator = validated_data.get('operator', instance.operator)
        instance.order = validated_data.get('order', instance.order)
        instance.type = validated_data.get('type', instance.type)
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        self._create_or_update_vars(instance, vars_data)
        return instance

    def _create_or_update_vars(self, parent_instance, vars_data):
        keep_vars = []
        for var_data in vars_data:
            var_id = var_data.get('id')
            if var_id:
                try:
                    var_instance = Condition.objects.get(id=var_id)
                    ConditionSerializer().update(var_instance, var_data)
                    keep_vars.append(var_instance.id)
                except Condition.DoesNotExist:
                    continue
            else:
                var_instance = ConditionSerializer().create(var_data)
                var_instance.parent = parent_instance
                var_instance.save()
                keep_vars.append(var_instance.id)
        
        # Delete vars not in the updated list
        for var in parent_instance.vars.all():
            if var.id not in keep_vars:
                var.delete()
        
        # Add or update vars
        parent_instance.vars.set(Condition.objects.filter(id__in=keep_vars))

    def to_internal_value(self, data):
        if isinstance(data, list):
            return [self.child.to_internal_value(item) for item in data]
        return super().to_internal_value(data)



class ActionSerializer(serializers.ModelSerializer):
    condition = ConditionSerializer()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Actions
        fields = '__all__'

    def create(self, validated_data):
        condition_data = validated_data.pop('condition')

        print(condition_data)

        condition = ConditionSerializer.create(ConditionSerializer(), validated_data=condition_data)
        action = Actions.objects.create(condition=condition, **validated_data)
        return action
    
    def update(self, instance, validated_data):
        condition_data = validated_data.get('condition', None)

        instance.details = validated_data.get('details', instance.details)
        instance.action = validated_data.get('action', instance.action)
        instance.order = validated_data.get('order', instance.order)

        instance.save()

        if condition_data and condition_data.get('id', None):
            condition_instance = Condition.objects.get(id=condition_data.get('id', None))
            ConditionSerializer.update(ConditionSerializer(), condition_instance, condition_data)
        else:
            condition_instance = ConditionSerializer.create(ConditionSerializer(), validated_data=condition_data)
            instance.condition = condition_instance
            instance.save()

        return instance
            

class LogicSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(many=True)
    id = serializers.IntegerField(required=False)

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
    
    def update(self, instance, validated_data):
        actions_data = validated_data.pop('actions', [])

        instance.ref = validated_data.get('ref', instance.ref)
        instance.type = validated_data.get('type', instance.type)
        instance.order = validated_data.get('order', instance.order)

        instance.save()

        keep_actions = []
        for action_data in actions_data:
            if "id" in action_data.keys():
                if Actions.objects.filter(id=action_data["id"]).exists():
                    action = Actions.objects.get(id=action_data["id"])
                    ActionSerializer.update(ActionSerializer(), action, action_data)
                    keep_actions.append(action.id)
                else:
                    continue
            else:
                action_data['logic'] = instance
                action = ActionSerializer.create(ActionSerializer(), validated_data=action_data)
                keep_actions.append(action.id)

        instance.actions.exclude(id__in=keep_actions).delete()
        return instance   


class FieldPropertySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = FieldProperty
        fields = '__all__'
    
    def update(self, instance, validated_data):
        
        instance.allow_multiple_selection = validated_data.get('allow_multiple_selection', None)
        instance.randomize = validated_data.get('randomize', None)
        instance.allow_other_choice = validated_data.get('allow_other_choice', None)
        instance.vertical_alignment = validated_data.get('vertical_alignment', None)
        instance.supersized = validated_data.get('supersized', None)
        instance.show_labels =  validated_data.get('show_labels', None)
        instance.alphabetical_order =  validated_data.get('alphabetical_order', None)
        instance.button_text =  validated_data.get('button_text', None)
        instance.steps =  validated_data.get('steps', None)
        instance.shape =  validated_data.get('shape', None)
        instance.start_at_one =  validated_data.get('start_at_one', None)
        instance.choices =  validated_data.get('choices', None)
        instance.lables =  validated_data.get('lables', None)

        instance.save()

        return instance

class FieldSerializer(serializers.ModelSerializer):
    properties = FieldPropertySerializer()
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Field
        fields = '__all__'

    def create(self, validated_data):
        properties_data = validated_data.pop('properties')
        field_property = FieldProperty.objects.create(**properties_data)
        field = Field.objects.create(properties=field_property, **validated_data)
        return field
    
    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', None)
        instance.description = validated_data.get('description', None)
        instance.ref = validated_data.get('ref', None)
        instance.type = validated_data.get('type', None)
        instance.layout = validated_data.get('layout', None)
        instance.order =  validated_data.get('order', None)

        instance.save()


        if instance.properties:
            FieldPropertySerializer.update(FieldPropertySerializer(), instance.properties, validated_data.get('properties', None))
        else:
            FieldPropertySerializer.create(instance.properties, validated_data.get('properties', None))
        
        return instance

class FormSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)
    logic = LogicSerializer(many=True)

    class Meta:
        model = Form
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        fields_data = validated_data.pop('fields')
        logic_data = validated_data.pop('logic')

        form = Form.objects.create(**validated_data)
        for field_data in fields_data:
            field_data['form'] = form
            FieldSerializer.create(FieldSerializer(), validated_data=field_data)
        for logic_data_item in logic_data:
            logic_data_item['form'] = form
            LogicSerializer.create(LogicSerializer(), validated_data=logic_data_item)
        return form
    
    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', [])
        logic_data = validated_data.pop('logic', [])

        instance.title = validated_data.get('title', instance.title)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()

        keep_fields = []
        for field_data in fields_data:

            # since field is connected as common FK relation with property need a proper way, IDK what to do here as of now
            properties = field_data.get('properties', None)
            field_id = properties.get('id', None) if properties else None
            if field_id and Field.objects.filter(pk=field_id).exists():
                field_instance = Field.objects.get(pk=field_id)
                FieldSerializer.update(FieldSerializer(), field_instance, field_data)
                keep_fields.append(field_instance.pk)
            else:
                field_data['form'] = instance
                field_instance = FieldSerializer.create(FieldSerializer(), validated_data=field_data)
                keep_fields.append(field_instance.id)

        instance.fields.exclude(pk__in=keep_fields).delete()

        keep_logics = []
        for logic_data_item in logic_data:
            logic_id = logic_data_item.get('id')
            if logic_id and Logic.objects.filter(id=logic_id).exists():
                logic_instance = Logic.objects.get(id=logic_id)
                LogicSerializer.update(LogicSerializer(), logic_instance, logic_data_item)
                keep_logics.append(logic_instance.id)
            else:
                logic_data_item['form'] = instance
                logic_instance = LogicSerializer.create(LogicSerializer(), validated_data=logic_data_item)
                keep_logics.append(logic_instance.id)

        instance.logic.exclude(id__in=keep_logics).delete()

        return instance