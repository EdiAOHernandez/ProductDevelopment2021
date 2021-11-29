library(shiny)

shinyUI(fluidPage(
    
    # Application title
    titlePanel("Shiny Plots"),
    
    tabsetPanel(
        
        tabPanel('Interacción con Plots',
                 plotOutput("plot_click_option",
                            click = 'clk',
                            dblclick = 'dclk',
                            hover = 'mouse_hover',
                            brush = 'mouse_brush'),
                 verbatimTextOutput('click_data'),
                 tableOutput('mtcars_tbl')
        )
    )
))
