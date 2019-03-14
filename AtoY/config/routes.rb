Rails.application.routes.draw do
  devise_for :users, module: :users, controllers: {
        sessions: 'users/sessions'
      }
  root to: 'tools#home'
  get 'home', to: 'tools#home'
  get 'login', to: 'tools#login'
  get 'asin', to: 'tools#asin'
  get 'result', to: 'tools#result'
end
