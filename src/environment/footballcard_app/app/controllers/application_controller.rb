class ApplicationController < ActionController::Base

  def hello
    render html: "This is the third chapter greeting."
  end
end
