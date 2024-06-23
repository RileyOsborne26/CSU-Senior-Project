class CreatePriceHistories < ActiveRecord::Migration[7.0]
  def change
    create_table :price_histories, id: false do |t|
      t.primary_key :card_price_id
      t.references :user_card_id, null: false, foreign_key: { to_table: :owned_cards, primary_key: :user_card_id }
      t.datetime :price_date
      t.decimal :market_value, precision: 10, scale: 2

      t.timestamps
    end
  end
end
