class lecturas_db:


    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'lecturas_db':
            return 'lecturas_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'lecturas_db':
            return 'lecturas_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        if(
            obj1._meta.app_label == 'lecturas_db' or
            obj2._meta.app_label == 'lecturas_db'
        ):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'lecturas_db':
            return db == 'lecturas_db'
        return None