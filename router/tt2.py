def add_methods_and_instantiate(decorated_class, *args, **kwargs):
    class EnhancedClass(decorated_class):
        def __init__(self, *init_args, **init_kwargs):
            super().__init__(*init_args, **init_kwargs)

        # 假设我们想要为类添加一个名为my_method的新方法
        def my_method(self, arg1, arg2):
            return f"Result from EnhancedClass.my_method: {arg1}, {arg2}"

    # 直接实例化并返回
    return EnhancedClass(*args, **kwargs)

# 原始类
class OldObject:
    def __init__(self, value="Value of Property 1"):
        self.property1 = value

# 使用装饰器来增强旧类并实例化
new_reflective_obj = add_methods_and_instantiate(OldObject)
print(new_reflective_obj.my_method("value1", "value2"))  # 输出：Result from EnhancedClass.my_method: value1, value2

# 同时仍然保留了原始的属性和方法
print(new_reflective_obj.property1)  # 输出：Value of Property 1

# 如果OldObject有参数，可以通过add_methods_and_instantiate传递
custom_value_obj = add_methods_and_instantiate(OldObject, "Custom Value")