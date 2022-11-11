import re
import telebot
from easygoogletranslate  import EasyGoogleTranslate
import logging
import os 
import dotenv
from langdetect import detect



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')
logging.basicConfig(filename='runnerlogs.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

translator = EasyGoogleTranslate()

dotenv.load_dotenv()
token = str(os.getenv("token"))

bot=telebot.TeleBot(token=token)




@bot.message_handler(['start'])
def start_command(message):
    bot.reply_to(message,'Hello there! I\'m a bot. What\'s up? \n Do /help to see what i can do ')
@bot.message_handler(['help'])
def help_command(message):
    bot.reply_to(message,'/start - Starts the bot\n/Help - help command\n /translate to translate a text ')
    
    
@bot.message_handler(['translate'])
def translate_command(message):
    kknk=message.text.split()
    try:
       if kknk[1] == "":
           bot.reply_to(message,"wrong format use /translate <text to translate here>")
       else:
           text1 = str(message.text)
           text=re.sub('/translate','',text1)
           
           result = translator.translate(f'{(text)}', target_language='en')
           bot.reply_to(message,text=(f'{result}'))
    except:
        bot.reply_to(message,"wrong format use /translate <text to translate here>")
        
        

@bot.message_handler(content_types=['ERROR'])
def error(message):
    # Logs errors
    logging.error(f'Update {message} caused error {message.error}')
    
@bot.message_handler(['id'])
def handle_message(message):
    bot.send_message(message.chat.id,text=(f'This chat id is : `{message.chat.id}`'),parse_mode='MarkdownV2')
    
    
def stats(message):
    f=open("translation-ON.txt","r")
    k=str(f.read())
    op=re.findall("(.*):",k)
    print(op)
    if str(message.chat.id)  in str(op):
        return True 
    elif str(message.chat.id) not in str(op):
        return False
    else:
        return True
    
def saver(chetid,onf):
    dicdone=dicdone=(f'{chetid}:{onf}')
    if onf == "on":
        with open("translation-ON.txt","r") as f:
            print(str(chetid))
            f=open("translation-ON.txt","r")
            op=re.findall(".*",str(f.read()))
            for a in op:
                if str(dicdone) in a:
                    print("already on")
                    break
                else:
                    with open("translation-ON.txt","a") as f:
                        mk=f.write(f'{dicdone}\n')
    
    elif onf == "off":
                    with open("translation-ON.txt","w+") as f:
                        r=f.read()
                        koko=re.sub(f'{dicdone}','',r)
                        f.write(koko)
    
@bot.message_handler(commands=['auto'],chat_types=['group','supergroup'])
def handle_message(message):
    print(message.chat.type)
    
    adminsir=bot.get_chat_administrators(message.chat.id)
    idos=str(message.from_user.id)
    admons=adminsir[0]
    
    
    matches=re.findall("id': (..........),",str(admons))
    for a in matches:
        print(a)
        
        
        
        if idos == a:
           
            try:
                cond=message.text.split()
                
                print(cond,cond[1])
                chetid1=message.chat.id
                onf1=cond[1]
                onf1=onf1.lower()
                if cond[1]=="on":
                    bot.reply_to(message,"yes daddy auto translation is on")
                    saver(chetid1,onf1)
                    #return True
                    
                else:
                    saver(chetid1,onf1)
                    bot.reply_to(message,"ok boi auto translation off")
                    
                        
                        
                        
                    #return False
            except IndexError:
                wrongsyntax="USE CORRECT SYNTAX :\n`/auto on` \- turn on auto translation\n `/auto off` \-turn off auto translation "
                bot.send_message(message.chat.id, wrongsyntax, parse_mode='MarkdownV2')
        else:
            bot.send_message(message.chat.id,"GO AWAY PEASANT ,NON ADMINNN!!!!")
        print(stats(message))
            
            
      


def tr(message):
    text = str(message.text)
    dl=detect(f'{text}')
    print(dl)
    if dl == 'en':
        return
    else:
        result = translator.translate(f'{(text)}', target_language='en')
        
        
        logging.info(f'User @{message.from_user.username}({message.chat.id}) says: {text}\n\t\t\t\tTranslated to: {result}')           
    return result


    

   

@bot.message_handler(func=stats,content_types="text")
def handle_message(message):
    koko=tr(message)
    print(koko)
    bot.reply_to(message,str(koko))
     





if __name__ == '__main__':
    bot.infinity_polling(1.0)


