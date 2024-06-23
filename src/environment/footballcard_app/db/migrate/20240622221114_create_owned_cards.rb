class CreateOwnedCards < ActiveRecord::Migration[7.0]
  def change
    create_table :owned_cards, id: false do |t|
      t.primary_key :user_card_id
      t.references :user, null: false, foreign_key: { to_table: :users, primary_key: :user_id }
      t.references :card, null: false, foreign_key: { to_table: :cards, primary_key: :card_id }
      t.boolean :ownership_status
      t.datetime :date_created
      t.decimal :entry_market_value, precision: 10, scale: 2
      t.boolean :is_anonymous
      t.boolean :is_for_trade
      t.boolean :is_for_sale

      t.timestamps
    end
  end
end
