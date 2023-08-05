'''
Kangaroo versioning
'''
import yaml
import os


# singleton
class Singleton:
   __instance = None
   @staticmethod 
   def getInstance():
      ''' Static access method. '''
      if Singleton.__instance == None:
         Singleton()
      return Singleton.__instance
   def __init__(self):
      ''' Virtually private constructor. '''
      if Singleton.__instance != None:
         raise Exception(colored('This is a singleton!', 'red'))
      else:
         Singleton.__instance = self


class Kangaroo(Singleton):
    '''
Here to setup the build
    '''

    def __init__(self, project_name):
        super().__init__()
        self.build = 0
        self.version = 1.0
        self.path = ".%s.kangaroo" % project_name 
        self.project_name = project_name

        if not os.path.exists(self.path):
            self.config = {'build': self.build, 'version': self.version}
            self._write()

        with open(self.path, 'r+') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.build = config['build'] + 1
            self.version = config['version']
            self.config = {'build': self.build, 'version': self.version}
        # write the update .kangaroo version
            self._write()

    def _write(self):
        with open(self.path, 'w+') as f:
            f.write(yaml.dump(self.config))
    
    def show_logo(self):
        #TODO something
        pass

    def show_build(self):
        print("%s: v%s (%s)" % (self.project_name, self.version, self.build))
        

    def update_version(self, version):
        self.version = version
        with open(self.path, 'r+') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            self.config = {'build': self.build, 'version': self.version}
        # write the update .kangaroo version
        self._write()
