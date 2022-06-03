from copyreg import pickle
import pickle

def deserialize(obj):
    stream = pickle.loads(obj)
    return stream

def save_stream(stream, display=True):
    for message in stream.messages:
        with open(
                f'./recv/connection_{message.con_id}.csv', 'a'
                    ) as f:
                f.write(str(message))
                f.write("\n")
            
    if display:
        print(stream)
