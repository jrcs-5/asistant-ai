from modules.weather import Weather
from modules.pc_command import PcCommand
from modules.tv_controller import TVController

class CommandHandler:
    @staticmethod
    def create_command(action, args):
        
        print("accion: ",action,"\nargumentos: ",args)
        
        if action == "get_weather":
            return Weather().get_weather(args['location'])
        elif action == "send_email":
            return PcCommand().send_email(args['recipient'], args['subject'], args['body'])
        elif action == "open_chrome":
            return PcCommand().open_chrome(args['website'])
        elif action == "get_time":
            return PcCommand().get_time(args['location'])
        elif action == "control_television":
            tv = TVController ()
            tv.cargar()
            
            if args['action'] == "prender":
                return tv.prender()
            elif args['action'] == "apagar":
                return tv.apagar()
            elif args['action'] == "prender_play":
                return tv.prender_play()
            elif args['action'] == "mutear":
                return tv.mutear()
            elif args['action'] == "desmutear":
                return tv.desmutear()
            else:
                return None
        else:
            return None