class CreateOwnerHistories < ActiveRecord::Migration[7.0]
  def change
    create_table :owner_histories do |t|
      t.primary_key :user_card_id
      t.references :user_id, null: false, foreign_key: true
      t.references :card_id, null: false, foreign_key: true
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
