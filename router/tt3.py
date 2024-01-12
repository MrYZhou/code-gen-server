import dataset

db = dataset.connect('sqlite:///:memory:')

table = db['sometable']
table.insert(dict(name='John Doe', age=37))
table.insert(dict(name='Jane Doe', age=34, gender='female'))

john = table.find_one(name='John Doe')


def square(x):
    return x ** 2

def apply_function(func, arg):
    return func(arg)

result = apply_function(square, 3)  # 结果为9