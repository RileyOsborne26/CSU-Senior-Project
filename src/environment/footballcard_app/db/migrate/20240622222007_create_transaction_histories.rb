class CreateTransactionHistories < ActiveRecord::Migration[7.0]
  def change
    create_table :transaction_histories, id: false do |t|
      t.primary_key :transaction_id
      t.references :buyer_user_id, null: false, foreign_key: { to_table: :users, primary_key: :user_id } 
      t.references :user_card_id, null: false, foreign_key: { to_table: :owned_cards, primary_key: :user_card_id }
      t.integer :type
      t.datetime :transaction_date
      t.decimal :price, precision: 10, scale: 2

      t.timestamps
    end
  end
end
