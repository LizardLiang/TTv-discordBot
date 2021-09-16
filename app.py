from threading import Timer
import twitchapp
import os
import threading
del sys.modules['twitchapp']

groupid = ''

keep_run = True

s = sched.scheduler(time.time, time.sleep)


def do_something():
    global keep_run
    cnt = 0
    while keep_run:
        cnt = cnt + 1
        print('checking' + str(cnt))
        state = twitchapp.get_streams('nana803')
        # if state:
        #    line_bot_api.push_message('U58e43cf60b31e2ed4a101db4cab57fa6', TextSendMessage(state))
        #    time.sleep(10)

        state1 = tw1.get_streams('inkwei0108')
        if state and state1:
            message = state + '\n' + state1
            line_bot_api.push_message(
                'U58e43cf60b31e2ed4a101db4cab57fa6', TextSendMessage(message))
        elif state1:
            message = state1
            line_bot_api.push_message(
                'U58e43cf60b31e2ed4a101db4cab57fa6', TextSendMessage(message))
        elif state:
            message = state
            line_bot_api.push_message(
                'U58e43cf60b31e2ed4a101db4cab57fa6', TextSendMessage(message))

        # do your stuff
        time.sleep(10)


game_key = 0


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    t = threading.Thread(target=do_something)  # 這個就開一個新的thread 讓他自己玩得爽
    t.start()
    app.run(host='0.0.0.0', port=port)
