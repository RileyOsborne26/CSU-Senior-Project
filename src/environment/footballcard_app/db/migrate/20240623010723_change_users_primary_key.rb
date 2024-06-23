class ChangeUsersPrimaryKey < ActiveRecord::Migration[7.0]
  def change
    # Remove existing primary key (default)
    remove_column :users, :id

    add_column :users, :user_id, :primary_key

    add_index :users, :user_id, unique: true
  end
end
