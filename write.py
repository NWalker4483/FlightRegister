import os
colors={
"default" : "\033[0m",
"red" : "\033[91m",
"green" : "\033[92m",
"yellow" : "\033[93m",
"blue" : "\033[94m",
"purple" : 	"\033[95m"}
def writeout(*args,color='default', end='\n', sep='\n'):
    if os.name == 'posix':
        print(colors[color],end=''),
    try:
        if len(*args) > 0:
            for i in args:	print (i,end=end,sep=sep),
        print(colors['default'],end='')
    except:
        pass
    print(colors['default'],end='')
def RainbowPrint(String):
	for i in range(len(String)):
		writeout(String[i],end='',color=list(colors.keys())[i%6])
	print('')
if __name__ == "__main__":
    RainbowPrint('This is Amazing')

    writeout("Potato",color='blue')
