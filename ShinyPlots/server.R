library(shiny)
library(dplyr)
library(ggplot2)

shinyServer(function(input, output) {
    

    #output$plot_click_option <- renderPlot({
    #    plot(mtcars$wt,mtcars$mpg, xlab = 'wt', ylab = 'Millas x galon')
    #})
    
    TablaDF <- NULL
    HoverG <- NULL
    
    output$click_data <- renderPrint({
        list(
            click_xy = c(input$clk$x,input$clk$y),
            double_click_xy = c(input$dclk$x,input$dclk$y),
            hover_xy = c(input$mouse_hover$x,input$mouse_hover$y),
            brush_xy = c(input$mouse_brush$xmin,input$mouse_brush$ymin,
                         input$mouse_brush$xmax,input$mouse_brush$ymax)
        )
    })
    
    output$mtcars_tbl <- renderTable({
        df <- renderTable()
        #df <- nearPoints(mtcars,input$mouse_hover,xvar = 'wt', yvar = 'mpg')
        #df <- brushedPoints(mtcars,input$mouse_brush,xvar = 'wt', yvar = 'mpg')
        df
        ##df2
    })

    
    
    output$plot_click_option <- renderPlot({
        plot(mtcars$wt,mtcars$mpg, xlab="wt", ylab = "Millas x galon",cex=1.5)
        if (!is.null(input$clk$x)){
            df<-nearPoints(mtcars,input$clk,xvar='wt',yvar='mpg')
            out <- df %>% 
                select(wt,mpg)
            TablaDF <<- rbind(TablaDF,out) %>% distinct()
        }
        
        if(!is.null(input$dclk$x)){
            df<-nearPoints(mtcars,input$dclk,xvar='wt',yvar='mpg')
            out <- df %>% 
                select(wt,mpg)
            TablaDF <<- setdiff(TablaDF,out)
        }
        
        if(!is.null(input$mouse_hover$x)){
            df<-nearPoints(mtcars,input$mouse_hover,xvar='wt',yvar='mpg')
            out <- df %>% 
                select(wt,mpg)
            HoverG <<- out
        }
        
        if(!is.null(input$mouse_brush)){
            df<-brushedPoints(mtcars,input$mouse_brush,xvar='wt',yvar='mpg')
            out <- df %>% 
                select(wt,mpg)
            TablaDF <<- rbind(TablaDF,out) %>% 
                dplyr::distinct()
        }
        if(!is.null(HoverG)){
            points(HoverG[,1],HoverG[,2],col='gray',pch=16,cex=3)
        }
        if(!is.null(TablaDF)){
            points(TablaDF[,1],TablaDF[,2],col='green',pch=16,cex=2)
        }
    })
    
    
    renderTable <- reactive({
        input$clk$x
        input$dclk$x
        input$mouse_brush
        TablaDF
    })
    

})