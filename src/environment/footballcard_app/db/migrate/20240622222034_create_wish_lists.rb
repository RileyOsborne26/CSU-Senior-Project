class CreateWishLists < ActiveRecord::Migration[7.0]
  def change
    create_table :wish_lists, id: false do |t|
      t.primary_key :wish_id
      t.references :user_id, null: false, foreign_key: { to_table: :users, primary_key: :user_id }
      t.references :card_id, null: false, foreign_key: { to_table: :cards, primary_key: :card_id }

      t.timestamps
    end
  end
end
