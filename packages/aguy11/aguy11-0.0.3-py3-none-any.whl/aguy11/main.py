import random
import json
import urllib.requests
def advice(display):
  try:
    display = bool(display)
  except TypeError:
    print("ERR: display paramenter must be bool")
  url = 'https://api.adviceslip.com/advice'
  request = urllib.requests.urlopen(url)
  result = json.loads(request.read())
  endpoint = result['slip']['advice']
if display:
  print(endpoint)
  return endpoint
else:
  return endpoint

def makeascii(model, display):
  if model == "fish":
    r = '''      /`·.¸
     /¸...¸`:·
 ¸.·´  ¸   `·.¸.·´)
: © ):´;      ¸  {
 `·.¸ `·  ¸.·´\`·¸)
     `\\´´\¸.·´'''
  elif model == "cat":
    r = '''
    |\__/,|   (`\
  _.|o o  |_   ) )
-(((---(((--------'''
  elif model == "wolf":
    r = '''                              __
                            .d$$b
                          .' TO$;\
                         /  : TP._;
                        / _.;  :Tb|
                       /   /   ;j$j
                   _.-"       d$$$$
                 .' ..       d$$$$;
                /  /P'      d$$$$P. |\
               /   "      .d$$$P' |\^"l
             .'           `T$P^"""""  :
         ._.'      _.'                ;
      `-.-".-'-' ._.       _.-"    .-"
    `.-" _____  ._              .-"
   -(.g$$$$$$$b.              .'
     ""^^T$$$P^)            .(:
       _/  -"  /.'         /:/;
    ._.'-'`-'  ")/         /;/;
 `-.-"..--""   " /         /  ;
.-" ..--""        -'          :
..--""--.-"         (\      .-(\
  ..--""              `-\(\/;`
    _.                      :
                            ;`-
                           :\
                           ;'''
  elif model == "egypt":
    r = '''                          _  ,~~~~~~~~~~,
                         9>)(_______     \
                          (()_____   /    )_
                           /     ///  / /)(()
                           |--    //___ \)())
                           )c>-    ___    )())
                          /      s)_     )  (()
                          `      " _     )   ())
                           >     /  _   )    (()
                           L____/    -_)     ())
                              \      |      (()
                               \      \    (()
                                \      \   ())
                                _\    _<7\ (()
       )                      .-<-7\7\ ())
       (                     //'''
  elif model == 'yoda':
    r = '''                    ____
                 _.' :  `._
             .-.'`.  ;   .'`.-.
    __      / : ___\ ;  /___ ; \      __
  ,'_ ""--.:__;".-.";: :".-.":__;.--"" _`,
  :' `.t""--.. '<@.`;_  ',@>` ..--""j.' `;
       `:-.._J '-.-'L__ `-- ' L_..-;'
         "-.__ ;  .-"  "-.  : __.-"
             L ' /.------.\ ' J
              "-.   "--"   .-"
             __.l"-:_JL_;-";.__
          .-j/'.;  ;""""  / .'\"-.
        .' /:`. "-.:     .-" .';  `.
     .-"  / ;  "-. "-..-" .-"  :    "-.
  .+"-.  : :      "-.__.-"      ;-._   \
  ; \  `.; ;                    : : "+. ;
  :  ;   ; ;                    : ;  : \:
 : `."-; ;  ;                  :  ;   ,/;
  ;    -: ;  :                ;  : .-"'  :
  :\     \  : ;             : \.-"      :
   ;`.    \  ; :            ;.'_..--  / ;
   :  "-.  "-:  ;          :/."      .'  :
     \       .-`.\        /t-""  ":-+.   :
      `.  .-"    `l    __/ /`. :  ; ; \  ;
        \   .-" .-"-.-"  .' .'j \  /   ;/
         \ / .-"   /.     .'.' ;_:'    ;
          :-""-.`./-.'     /    `.___.''''
  elif model == 'pikachu':
    r = '''`;-.          ___,
  `.`\_...._/`.-"`
    \        /      ,
    /()   () \    .' `-._
   |)  .    ()\  /   _.'
   \  -'-     ,; '. <
    ;.__     ,;|   > \
   / ,    / ,  |.-'.-'
  (_/    (_/ ,;|.<`
    \    ,     ;-`
     >   \    /
    (_,-'`> .'
         (_,''''     
  else:
    print("Invalid ASCII request")
  try:
    display = bool(display)
  except TypeError:
    print('ERR: Display paramenter must be bool')
    quit()
  if display:
    print(r)
    return r
  else:
    return r
def volume(x, y, z, display):
  try:
    display = bool(display)
  except TypeError:
    print('ERR: Display paramenter must be bool')
    quit()
  vol = x * y * z
  if display:
    print(vol)
    return vol
  else:
    return vol

def astros_current(display):
  try:
    display = bool(display)
  except TypeError:
    print('ERR: Display paramenter must be bool')
    quit()
  url = "http://api.open-notify.org/astros.json"
  response = urllib.request.urlopen(url)
  result = json.loads(response.read())
  number = result["number"]
  if display:
    print(number)
    return number
  else:
    return number

def rhyme(display, word):
  try:
    display = bool(display)
  except TypeError:
    print('ERR: Display paramenter must be bool')
    quit()
  url = 'http://api.datamuse.com/words?rel_rhy=' + word
  response = urllib.request.urlopen(url)
  result = json.loads(response.read())
  rhyme = result[0]['word']
  if display:
    print(rhyme)
    return rhyme
  else:
    return rhyme

def corona(display, state):
  try:
    display = bool(display)
  except TypeError:
    print('ERR: Display paramenter must be bool')
    quit()
  url = 'http://coronavirusapi.com/getTimeSeriesJson/' + state
  response = urllib.request.urlopen(url)
  result = json.loads(response.read())
  confirmed = result[-1]["positive"]
  deaths = result[-1]["deaths"]
  tested = result[-1]["tested"]
  secs = result[-1]["seconds_since_epoch"]
  alls = [comnfirmed, deaths, tested, secs]
  if display:
    print(alls)
    return alls
  else:
    return alls
  
