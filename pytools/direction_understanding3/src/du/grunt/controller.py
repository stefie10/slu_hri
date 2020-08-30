import utbot

def main():
    bot = utbot.utbot()
    bot.spawn_bot("USARBot.MDS",(-7.68,-21.44,18.24), (0, 0, 1.58))
    #bot.spawn_bot("USARBot.P2AT",(-7.68,-21.44,18.24), (0, 0, 1.58))
    #bot.spawn_bot("USARBot.MultiView",(-7.68,-21.44,18.24), (0, 0, 1.58))
    #bot.pause()

    while True:
        bot.update()
        #print "pose", bot.pose
if __name__=="__main__":
    main()
