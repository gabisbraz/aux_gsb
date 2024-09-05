# Agrupa o df_combined por AGENCIA para acesso rápido
agencia_groups = {
    agencia: df_agencia for agencia, df_agencia in df_combined.groupby("AGENCIA")
}

# Pré-computa os ícones e cores do farol para acesso rápido
farol_cache = {
    farol_value: score_farol_map.get(
        farol_value, {"color": "white", "icon": "bi bi-circle-fill"}
    )
    for farol_value in df_combined["FAROL"].unique()
}

# Pré-processa os temas dos pilares
pilar_tema_map = {
    pilar: list(dataframe[pilar].columns)
    for pilar in ordem_pilares
    if pilar in dataframe.columns.levels[0]
}

# Itera sobre as linhas do dataframe
dataframe_aux = dataframe.to_dict("index")
for index_values, row_data in dataframe_aux.items():
    # Inicia uma nova linha na tabela
    html_string += "<tr>"

    # Adiciona índice à linha
    for index_column in index_values:
        html_string += f"<td class='index'>{index_column}</td>"

    # Recupera o dataframe da agencia correspondente do grupo
    df_agencia = agencia_groups.get(index_values[0], pd.DataFrame())

    # Itera sobre os pilares
    for pilar, temas in pilar_tema_map.items():
        # Itera sobre os temas de cada pilar
        for tema in temas:
            # Obtém o valor da célula, ou 0 se não existir
            valor = row_data.get((pilar, tema), 0)

            # Recupera ícone e cor do farol, se disponível
            df_agencia_pilar_tema = df_agencia[
                (df_agencia["PILAR"] == pilar) & (df_agencia["TEMA"] == tema)
            ]
            icone_color = None
            icone_score = None
            if not df_agencia_pilar_tema.empty:
                farol_value = df_agencia_pilar_tema["FAROL"].values[0]
                icone_color = farol_cache[farol_value]["color"]
                icone_score = farol_cache[farol_value]["icon"]

            try:
                valor = f"{valor:.2f}"
            except Exception:
                valor = "-"
                icone_color = None
                icone_score = None

            # Adiciona a célula com o ícone e o valor
            html_string += (
                f'<td data-column="{pilar}-{tema}" style="color: black; text-align: center; min-width: 50px;">'
                f'<div style="display: flex;">'
                f'<div style="width: 50%; display: flex; justify-content: flex-end;">'
                f'<span class="{icone_score}" style="color: {icone_color}; padding-right: 5px;"></span>'
                f"</div>"
                f'<div style="width: 50%; display: flex; justify-content: flex-start;">{valor}</div>'
                f"</div></td>"
            )

    # Fecha a linha da tabela
    html_string += "</tr>"
