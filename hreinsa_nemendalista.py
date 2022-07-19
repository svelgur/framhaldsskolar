import csv
import click
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)


@click.command()
@click.argument("skra_inn", type=click.Path(exists=True))
@click.argument("skra_ut", type=click.Path(exists=False))
@click.option("-afmarkari", default=";", help="sjálfgefið: ;")
@click.option(
    "-ar",
    default=2022,
    help="ár til útreiknings á aldri frá kennitölu, sjálfgefið: 2022",
)
def hreinsa_skra(skra_inn, skra_ut, afmarkari, ar):
    """Hreinsar SKRA_INN og skrifar út í nýja skrá: SKRA-UT."""
    click.echo("Hreinsa skrá: {}".format(skra_inn))
    # sleppum fyrstu línu - ætti kannski að vera option
    df = pd.read_csv(skra_inn, sep=afmarkari, header=1)
    # búum til eininga dálk
    df["einingar"] = df["Ein.á önn - þrep"] + (df["Ein.á önn"] * (30 / 17.5))
    # röðum eftir kennitölu og einingum
    df.sort_values(by=["Kennitala", "einingar"], inplace=True)
    # búum til heimaskóla dálk (0/1) eftir hæsta fjölda eininga fyrir kennitölu
    df["heimaskoli"] = df.duplicated("Kennitala", keep="first").astype(int)

    # finnum út aldur út frá kt
    # df["old"] = df[df["Kennitala"].astype(str)].str.endswith("0")

    df["old"] = np.where(
        df["Kennitala"].astype(str).str.endswith("0") == True, 2000, 1900
    )
    df["faedingarar"] = df["Kennitala"].astype(str).str.slice(3, 5)
    df["aldur_2"] = int(ar) - (df["old"].astype(int) + df["faedingarar"].astype(int))
    df.drop(["old", "faedingarar"], axis=1, inplace=True)

    df.to_csv(skra_ut)
    click.echo("Skrifaði skrá: {}".format(skra_ut))


if __name__ == "__main__":
    hreinsa_skra()
