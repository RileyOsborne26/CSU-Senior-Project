class ModifyUsersAddLastNameAddUsername < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :username, :string, limit: 25
    add_column :users, :last_name, :string, limit: 25

    add_index :users, :username, unique: true
  end
end
