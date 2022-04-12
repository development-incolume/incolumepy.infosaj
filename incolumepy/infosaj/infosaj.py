"""infosaj Module."""

__author__ = "@britodfbr"

import logging
import os
from datetime import datetime
from pathlib import Path
from random import randint

import yaml
from bs4 import BeautifulSoup
from faker import Faker

htmlskel = (
    '<!DOCTYPE html><html lang="pt-br">'
    "<head>"
    '<meta name="viewport" '
    'content="width=device-width, initial-scale=1">'
    '<meta charset="UTF-8">'
    "<title>Informativo SAJ</title>"
    "<style>"
    '@import url("css/color.css");'
    '@import url("css/layout.css");'
    "</style>"
    "</head>"
    "<body>"
    "<header>"
    "</header>"
    "</body>"
    "</html>"
)

modelfile = Path.home().joinpath("infosaj", "model.yaml")

fake = Faker("pt_BR")
Faker.seed(13)
aniversariantes = [(fake.date_this_month(), fake.name()) for x in range(20)]
datamodel = {
    "infodate": fake.date_object(),
    "infonum": randint(1, 10),
    "footer": [None, None, "IMG/acesso-a-infornacao.png"],
    "htmlname": "index.html",
    "aniversariantes": aniversariantes,
    "decisões": [
        {
            "title": f"ADI {x} Medida Cautelar",
            "relator": fake.name(),
            "resumo": fake.sentence(),
            "message": None,
            "linkaddress": "#",
            "linktext": fake.uri(),
        }
        for x in range(5)
    ],
}


def gen_model_conf():
    temp = os.environ.get("INCOLUMEPY_INFOSAJ")
    file = Path(temp).with_name("model.yaml") if temp else modelfile
    file.parent.mkdir(parents=True, exist_ok=True)
    result = "#! Arquivo de configuração para o" " 'informativo SAJ'\n".encode(
        "iso8859-1"
    ) + yaml.dump(datamodel, sort_keys=False, encoding="iso8859-1")
    logging.debug(file)
    file.write_bytes(result)
    logging.debug(result)
    return file


def gen_infosaj(file: Path = None):
    meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez",
    }

    temp = os.environ.get("INCOLUMEPY_INFOSAJ")
    fin = Path(temp).with_name("model.yaml") if temp else modelfile
    content = yaml.full_load(fin.read_text(encoding="iso8859-1"))
    print(content)
    html = BeautifulSoup(htmlskel, "html5lib")
    html.header.append(html.new_tag("figure"))
    html.header.figure.append(
        html.new_tag(
            "img", attrs={"src": "IMG/Header_teste_1-03.png", "width": "100%"}
        )
    )
    html.body.append(html.new_tag("span", attrs={"class": "num"}))
    html.body.span.string = (
        "Brasília/DF, "
        f"{meses[content['infodate'].month]}/"
        f"{content['infodate'].year} - Nº {content['infonum']}"
    )

    html.body.append(html.new_tag("h2"))
    html.body.h2.string = "Decisões Judiciais Relevantes"

    # decisoes
    for i, decisoes in enumerate(content["decisões"], start=1):
        print(i, decisoes)
        html.body.append(html.new_tag("div"))
        html.body.select_one(f"div:nth-of-type({i})").append(
            html.new_tag("h3")
        )
        html.body.select_one(f"div:nth-of-type({i})").h3.string = decisoes[
            "title"
        ]
        html.body.select_one(f"div:nth-of-type({i})").append(
            html.new_tag("span", attrs={"id": "relator"})
        )
        html.body.select_one(
            f"div:nth-of-type({i})"
        ).span.string = f'Relator(a): {decisoes["relator"]}'
        html.body.select_one(f"div:nth-of-type({i})").append(html.new_tag("p"))
        html.body.select_one(f"div:nth-of-type({i})").p.string = decisoes[
            "resumo"
        ]
        link = decisoes.get("linkaddress")
        msg = decisoes.get("message")
        if link:
            html.body.select_one(f"div:nth-of-type({i})").append(
                html.new_tag("span", attrs={"id": "link"})
            )
            a = html.new_tag("a", attrs={"href": link})
            a.string = decisoes.get("linktext")
            html.body.select_one(f"div:nth-of-type({i})").select_one(
                "#link"
            ).append("Para leitura completa acesse:")
            if msg:
                html.body.select_one(f"div:nth-of-type({i})").select_one(
                    "#link"
                ).string = msg
            html.body.select_one(f"div:nth-of-type({i})").select_one(
                "#link"
            ).append(a)
        html.body.append(html.new_tag("hr"))

    # Aniversariantes
    html.body.append(html.new_tag("div", attrs={"class": "aniversariantes"}))
    html.body.select_one(".aniversariantes").append(html.new_tag("h2"))
    html.body.select_one(
        ".aniversariantes"
    ).h2.string = "Aniversariantes do Mês"

    # table
    html.body.select_one(".aniversariantes").append(html.new_tag("table"))
    tabletitle = html.new_tag("thead")
    tabletitle.append(html.new_tag("tr"))
    tabletitle.tr.append(html.new_tag("th"))
    tabletitle.tr.append(html.new_tag("th"))
    html.select_one(".aniversariantes").table.append(tabletitle)
    html.select_one(".aniversariantes").table.append(html.new_tag("caption"))
    html.body.select_one(".aniversariantes").table.caption.string = (
        "Aniversariantes SAJ — "
        f'{meses[content["infodate"].month]}/{content["infodate"].year}'
    )
    html.select_one(".aniversariantes").table.append(html.new_tag("tbody"))
    html.select_one(".aniversariantes").table.append(html.new_tag("tfoot"))
    for date, name in sorted(content["aniversariantes"]):
        print(date.strftime("%d/%m"), name)
        row = html.new_tag("tr")
        row.append(html.new_tag("td"))
        row.append(html.new_tag("td"))
        row.select_one("td:nth-of-type(1)").append(date.strftime("%d/%m"))
        row.select_one("td:nth-of-type(2)").append(name)
        html.select_one(".aniversariantes").table.tbody.append(row)

    # Footer
    html.body.append(html.new_tag("footer"))
    for i, elem in enumerate(content["footer"], start=1):
        # print(i, elem)
        html.footer.append(html.new_tag("div"))
        if elem:
            html.footer.select_one(f"div:nth-of-type({i})").append(
                html.new_tag("figure")
            )
            html.footer.select_one(f"div:nth-of-type({i})").figure.append(
                html.new_tag("img", attrs={"src": elem})
            )

    filename = Path(__file__).with_name(
        content.get("htmlname") or "index.html"
    )
    filename.write_bytes(html.prettify(encoding="iso8859-1"))
    return filename.as_posix()


if __name__ == "__main__":  # pragma: no cover
    # gen_infosaj(Path('/tmp/test_load_model_envvar/model.yaml'))
    gen_model_conf()
    gen_infosaj()
