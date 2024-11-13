macro_micro = [
    ("macrocoluna1", "coluna01"),
    ("macrocoluna1", "coluna02"),
    ("macrocoluna1", "coluna03"),
    ("macrocoluna1", "coluna04"),
    ("macrocoluna2", "coluna05"),
    ("macrocoluna2", "coluna06"),
    ("macrocoluna2", "coluna07"),
    ("macrocoluna2", "coluna08"),
    ("macrocoluna2", "coluna09"),
    ("macrocoluna3", "coluna10"),
    ("macrocoluna3", "coluna11"),
    ("macrocoluna3", "coluna12"),
    ("macrocoluna3", "coluna13"),
    ("macrocoluna4", "coluna14"),
    ("macrocoluna4", "coluna15"),
    ("macrocoluna4", "coluna16"),
    ("macrocoluna4", "coluna17"),
    ("macrocoluna4", "coluna18"),
    ("macrocoluna5", "coluna19"),
    ("macrocoluna5", "coluna20"),
    ("macrocoluna5", "coluna21"),
    ("macrocoluna5", "coluna22"),
    ("macrocoluna5", "coluna23"),
    ("macrocoluna5", "coluna24"),
    ("macrocoluna5", "coluna25"),
]
macro = [
    "macrocoluna1"
    "macrocoluna1"
    "macrocoluna1"
    "macrocoluna1"
    "macrocoluna2"
    "macrocoluna2"
    "macrocoluna2"
    "macrocoluna2"
    "macrocoluna2"
    "macrocoluna3"
    "macrocoluna3"
    "macrocoluna3"
    "macrocoluna3"
    "macrocoluna4"
    "macrocoluna4"
    "macrocoluna4"
    "macrocoluna4"
    "macrocoluna4"
    "macrocoluna5"
    "macrocoluna5"
    "macrocoluna5"
    "macrocoluna5"
    "macrocoluna5"
    "macrocoluna5"
    "macrocoluna5"
]
micro = [
    "coluna01"
    "coluna02"
    "coluna03"
    "coluna04"
    "coluna05"
    "coluna06"
    "coluna07"
    "coluna08"
    "coluna09"
    "coluna10"
    "coluna11"
    "coluna12"
    "coluna13"
    "coluna14"
    "coluna15"
    "coluna16"
    "coluna17"
    "coluna18"
    "coluna19"
    "coluna20"
    "coluna21"
    "coluna22"
    "coluna23"
    "coluna24"
    "coluna25"
]

macro_unique = list(set(macro))


macro_colunas_default = ["macrocoluna4", "macrocoluna2"]
colunas_macro_adicionar_ao_usuario = ["macrocoluna5"]

macro_usuario = macro_colunas_default + colunas_macro_adicionar_ao_usuario

macro_micro_atualizada = [pair for pair in macro_micro if pair[0] in macro_usuario]

macro_atualizada = []
for macro, micro in macro_micro_atualizada:
    macro_atualizada.append(macro)

micro_atualizada = [pair[1] for pair in macro_micro_atualizada]

macro_unique_atualizada = []
for pair in macro_micro_atualizada:
    if pair[0] not in macro_unique_atualizada:
        macro_unique_atualizada.append(pair[0])

print(1)


def get_colunas(macro_micro_atualizada, macro_unique_atualizada):
    colunas = []

    for macro in macro_unique_atualizada:
        for pair in macro_micro_atualizada:
            if pair[0] == macro:
                colunas.append(pair[1])

    return colunas


col = get_colunas(macro_micro_atualizada, macro_unique_atualizada)

print(1)
