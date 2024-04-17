class ApplicationController < ActionController::Base
  include SessionsHelper

  def hello
    render html: "This is the third chapter greeting."
  end
end
