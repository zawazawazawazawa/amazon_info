class ToolsController < ApplicationController

    def home
        
    end

    def login

    end

    def asin
        
    end

    def postasin
        @asin = params[:asin]
        redirect_to result
    end

    def result
        
    end
end
