def print_func(name):
     if isinstance(name,list):
             for each_item in name:
                     print_func(each_item)
     else:
             print(name)
        
