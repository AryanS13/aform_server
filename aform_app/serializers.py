from rest_framework import serializers
from .models import Form, Field, FieldProperty, Logic, Actions, Condition

class VarSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        print(instance)
        return super().to_representation(instance)
    class Meta:
        model = Condition
        # fields = ('operator', 'order', 'type', 'value', 'vars', )
        fields = '__all__'
    
    def is_valid(self, data):
        print(data)
            
class ConditionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # vars 

    class Meta:
        model = Condition
        fields = ('id', 'operator', 'order', 'type', 'value', 'vars', )
    
    def get_fields(self):
        fields = super(ConditionSerializer, self).get_fields()
        fields['vars'] = ConditionSerializer(many=True, required=False, allow_null=True)
        return fields

    def create(self, validated_data):
        vars_data = validated_data.pop('vars', [])
        condition = Condition.objects.create(**validated_data)

        condition_vars = []
        for var_data in vars_data:
            var_instance = ConditionSerializer().create(var_data)
            var_instance.parent = condition
            var_instance.save()
            condition_vars.append(var_instance)

        condition.vars.set(condition_vars)
        return condition

    def update(self, instance, validated_data):
        vars_data = validated_data.pop('vars', [])
        instance.operator = validated_data.get('operator', instance.operator)
        instance.type = validated_data.get('type', instance.type)
        instance.value = validated_data.get('value', instance.value)
        instance.save()

        keep_vars = []
        for var_data in vars_data:
            if "id" in var_data.keys():
                if Condition.objects.filter(id=var_data["id"]).exists():
                    var = Condition.objects.get(id=var_data["id"])
                    var.operator = var_data.get('operator', var.operator)
                    var.type = var_data.get('type', var.type)
                    var.value = var_data.get('value', var.value)
                    var.save()
                    keep_vars.append(var.id)
                else:
                    continue
            else:
                var = Condition.objects.create(**var_data)
                var.parent = instance
                var.save()
                keep_vars.append(var.id)

        instance.vars.exclude(id__in=keep_vars).delete()
        return instance



class ActionSerializer(serializers.ModelSerializer):
    condition = ConditionSerializer()
    id = serializers.IntegerField(read_only=True)

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
        condition = validated_data.get('condition', None)

        instance.details = validated_data.get('details', None)
        instance.action = validated_data.get('action', 'jump')
        instance.order = validated_data.get('order', None)

        instance.save()


        if condition and condition.get('id', None):
            condition_ = Condition.objects.get(id=condition.get('id', None), condition=instance)
            ConditionSerializer.update(ConditionSerializer(), condition_, condition)
        else:
            condition_ = ConditionSerializer.create(condition)
            instance.condition = condition_
            instance.save()
        
        return instance
            

class LogicSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(many=True)
    id = serializers.IntegerField(read_only=True)

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
        actions_data = validated_data.get('actions', None)
       

        instance.ref = validated_data.get('ref', None)
        instance.type = validated_data.get('type', None)
        instance.order =  validated_data.get('order', None)

        instance.save()

        # Update or create actions
        for action_data in actions_data:
        

            action_id = action_data.get('id')
            if action_id:
                action_instance = Actions.objects.get(id=action_id, logic=instance)
                ActionSerializer.update(ActionSerializer(), instance=action_instance, validated_data=action_data)
            else:
                action_data['logic'] = instance
                ActionSerializer.create(ActionSerializer(), validated_data=action_data)
        


class FieldPropertySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
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
    # id = serializers.IntegerField(read_only=True)

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
        fields_data = validated_data.pop('fields', None)
        logic_data = validated_data.pop('logic', None)

        instance.title = validated_data.get('title', None)
        instance.organization = validated_data.get('organization', None)
        instance.save()

        for field_data in fields_data:
           
            property = field_data.get('properties')

            id = property.get('id', None)

            field_data['id'] = id

            print('My id is propertys', id)

            field = Field.objects.get(pk=id)

            if field is not None:
                # Update existing object
                FieldSerializer.update(FieldSerializer(), instance=field, validated_data=field_data)
            else:
                #Create new Field object 
                field_data['form'] = instance
                FieldSerializer.create(FieldSerializer(), field_data)
    
        for logic_item in logic_data:
            id = logic_item.get('id', None)
            logic = Logic.objects.get(pk=id)

            if logic is not None:
                # Update existing object
                LogicSerializer.update(LogicSerializer(), instance=logic, validated_data=logic_item)
            else:
                #Create new Field object
                logic_item['form'] = instance
                LogicSerializer.create(LogicSerializer(), logic_item)
        
        return instance

