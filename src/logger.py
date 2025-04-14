from os import makedirs, listdir, name 

class Logger:
    save_path = "./"
    
    @staticmethod
    def checkFolder():
        try:
            if(name == 'nt'):
                if("save_logs" not in listdir("C:/Windows/Temp")):
                    makedirs("C:/Windows/Temp/save_logs")
                    Logger.save_path = "C:/Windows/Temp/save_logs/"
            else:
                makedirs("/tmp/save_logs")
                Logger.save_path = "/tmp/save_logs/"
        except:
            print("Logger is disabled!")
            