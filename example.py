
import concurrent.futures
from hipchat import MessageParser


#This function only prints output  
def multithread_json_printer(hip_chat_message):
    hip_parsed = MessageParser(hip_chat_message)
    print "input is:", hip_chat_message
    print "JSON output is:", hip_parsed.to_json()
    print ""

# operate with a result of parsing in the body of this function
# if u need to do smth with it using multithreading
def multithread_json_parser(hip_chat_message):
    hip_parsed = MessageParser(hip_chat_message)
    print "input is:", hip_chat_message
    json_str = hip_parsed.to_json()
    #N! do smth with json_str.....
    #N!
    #N! or return as a result to shared list:
    # return hip_parsed.to_json()

if __name__ == "__main__":
    hipChat_messages = ['@chris you around?', 'Good morning! (megusta) (coffee)']

    # returns in the order given
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(multithread_json_printer, hipChat_messages)
