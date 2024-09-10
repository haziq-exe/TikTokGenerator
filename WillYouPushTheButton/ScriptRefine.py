from ButtonFetch import ButtonFetch

def RefineScript(Positive, Negative):

    Script = ' '

    for i in range(len(Positive)):
        if i != len(Positive):
            Script += f'::_: {Positive[i]} but:_:: {Negative[i]}. Will you push the button?_:_:_  \n'

    return Script