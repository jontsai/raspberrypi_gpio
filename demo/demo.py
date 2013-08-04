from time import sleep

from agents import DemoRPiAgent

def main():
    agent = DemoRPiAgent()
    try:
        agent.start()
        while agent.is_alive():
            sleep(1)
    except KeyboardInterrupt:
        print 'Got KeyboardInterrupt'
    finally:
        agent.terminate()

if __name__ == '__main__':
    main()
