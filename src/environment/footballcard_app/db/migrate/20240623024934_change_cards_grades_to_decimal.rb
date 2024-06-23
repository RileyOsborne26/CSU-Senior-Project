class ChangeCardsGradesToDecimal < ActiveRecord::Migration[7.0]
  def change
    change_column :cards, :grade_number, :decimal, precision: 1, scale: 3
    change_column :cards, :corners_subgrade_number, :decimal, precision: 1, scale: 3
    change_column :cards, :surface_subgrade_number, :decimal, precision: 1, scale: 3
    change_column :cards, :edges_subgrade_number, :decimal, precision: 1, scale: 3
    change_column :cards, :centering_subgrade_number, :decimal, precision: 1, scale: 3
  end
end
