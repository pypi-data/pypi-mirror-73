import pandas as pd


def pivot_category_prices(prices_df):
    prices_df = pd.pivot_table(
        prices_df, index=["shipment_id"], columns=["category"], values=["price_in_eur", "initial_price_in_eur"]
    )
    prices_df.columns = ["_".join(col).strip() for col in prices_df.columns.values]

    return prices_df.rename(
        columns={
            "price_in_eur_arrival_fees": "arrival_fees_price",
            "price_in_eur_arrival_truck_freight": "arrival_truck_freight_price",
            "price_in_eur_customs": "customs_price",
            "price_in_eur_departure_fees": "departure_fees_price",
            "price_in_eur_departure_truck_freight": "departure_truck_freight_price",
            "price_in_eur_freight": "freight_price",
            "price_in_eur_insurance": "insurance_price",
            "price_in_eur_other": "other_price",
            "initial_price_in_eur_arrival_fees": "arrival_fees_initial_price",
            "initial_price_in_eur_arrival_truck_freight": "arrival_truck_freight_initial_price",
            "initial_price_in_eur_customs": "customs_initial_price",
            "initial_price_in_eur_departure_fees": "departure_fees_initial_price",
            "initial_price_in_eur_departure_truck_freight": "departure_truck_freight_initial_price",
            "initial_price_in_eur_freight": "freight_initial_price",
            "initial_price_in_eur_insurance": "insurance_initial_price",
            "initial_price_in_eur_other": "other_initial_price",
        }
    )


def pivot_category_purchase_prices(prices_df):
    prices_df = pd.pivot_table(prices_df, index=["shipment_id"], columns=["category"], values=["purchase_price_in_eur"])
    prices_df.columns = prices_df.columns.droplevel()
    return prices_df.rename(
        columns={
            "arrival_fees": "arrival_fees_purchase_price",
            "arrival_truck_freight": "arrival_truck_freight_purchase_price",
            "customs": "customs_purchase_price",
            "departure_fees": "departure_fees_purchase_price",
            "departure_truck_freight": "departure_truck_freight_purchase_price",
            "freight": "freight_purchase_price",
            "insurance": "insurance_purchase_price",
            "other": "other_purchase_price",
        }
    )
