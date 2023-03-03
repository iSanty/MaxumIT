class SaladilloRouter:


    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'Saladillo' or model._meta.app_label == 'api':
            return 'saladillo_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'Saladillo' or model._meta.app_label == 'api':
            return 'saladillo_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        if(
            obj1._meta.app_label == 'Saladillo' or
            obj2._meta.app_label == 'Saladillo'
        ):
            return True
        elif(
            obj1._meta.app_label == 'api' or
            obj2._meta.app_label == 'api'
        ):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'Saladillo' or app_label == 'api':
            return db == 'saladillo_db'
        return None