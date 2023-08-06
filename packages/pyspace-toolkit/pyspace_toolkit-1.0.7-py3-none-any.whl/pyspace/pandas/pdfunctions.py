# %%
import pandas as pd
import jsonlines


# %%
def filter_zero(dfout):
    dfout = dfout.loc[:, (dfout != 0).any(axis=0)]
    dfout = dfout.loc[(dfout != 0).any(axis=1), :]
    return dfout


# %%
def pdselect(df, config):
    
    if config == []:
        return df
    
    operators = {
        '>': lambda x, y: x > y, 
        '<': lambda x, y: x < y, 
        '>=': lambda x, y: x >= y, 
        '<=': lambda x, y: x <= y,
        '==': lambda x, y: x == y, 
        '!=': lambda x, y: x != y,  
    }
    
    df_columns = list(df.columns)
    
    _conditions = []
    
    for i in config:
        
        _operand1 = df[i[0]]
        
        if i[2] in df_columns:
            _operand2 = df[i[2]]
        else:
            _operand2 = i[2]
        
        if(i[1] in operators):
            _operator = operators[i[1]]
            _condition = _operator(_operand1, _operand2)
        else:
            _operator = _operand1
            for attr in i[1].split('.'):
                _operator = getattr(_operator, attr)
            _condition = _operator(_operand2)
        _conditions.append(_condition)
    
    pd_select_bool_vector = _conditions[0]
    for _condition in _conditions:
        pd_select_bool_vector = pd_select_bool_vector & _condition
    
    return df[pd_select_bool_vector]
    
    # pd_select(outputdf, [['Intent', 'str.contains', 'eczane'],
    #                      ['Intent-f1', '<', 0.9],
    #                      ['Intent', 'isin', ['ik_eczane']],
    #                     ])
    pass

def pddisplay(df, b=True):
    if(b):
        pd.set_option("display.max_rows", 3000)
        pd.set_option("display.max_colwidth", 300)
        display(df)
        pd.reset_option("display.max_rows")
        pd.reset_option("display.max_colwidth")


def read_doccano(jsonline_path, intent, mode='jsonl'):

    if mode != 'jsonl':
        return []

    if mode == 'jsonl':
        dftemp = []
        with jsonlines.open(jsonline_path , mode='r') as f:

            _f_jsonlines = []
            for line in f:
                _f_jsonlines.append(line)
            _f_jsonlines = sorted(_f_jsonlines, key=lambda x: x['id']) if 'id' in _f_jsonlines[0] else _f_jsonlines

            for line in _f_jsonlines:
                temp = []
                line_labels = sorted(line['labels'], key=lambda x:x[0])
                for l in line_labels:
                    temp.append({'label': l[2], 'word':line['text'][l[0]:l[1]]})

                assert line['text'] == " ".join(t['word'] for t in temp)
                dftemp.append((line['text'], temp, intent))

        df = pd.DataFrame(dftemp, columns=['Sentence', 'Labels', 'Intent'])
        return df


