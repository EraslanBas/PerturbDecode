annoCols<-list(GeneGroup=c(G0='#A6CEE3',
                           G1='#1F78B4',
                           G2='#B2DF8A',
                           G3='#33A02C', 
                           G4='#FB9A99', 
                           G5='#FDBF6F', 
                           G6='#FF7F00', 
                           G7='#CAB2D6',
                           G8='#6A3D9A', 
                           G9='#FFFF99', 
                           G10="#B5651D",
                           G11="black"),
                 # GuideGroup=c(K0="#1f77b4",
                 #              K1="#ff7f0e",
                 #              K2="#279e68",
                 #              K3="#d62728", 
                 #              K4="#aa40fc", 
                 #              K5="#8c564b"),
                NewGuideGroup=c(M2="#1f77b4",
                             M3="#ff7f0e",
                             M6="#279e68",
                             M5="#d62728", 
                             M1="#aa40fc", 
                             M4="#8c564b"),
                 NewGeneGroup=c(
                           GP_1='#FF7F00',
                           GP_2='#FFFF99', 
                           GP_3="#B5651D",
                           GP_4='#FDBF6F', 
                           GP_5='#FB9A99',
                           GP_6='#CAB2D6',
                           GP_7='#A6CEE3',
                           GP_8='#1F78B4',
                           GP_9='#33A02C',
                           GP_10='#B2DF8A',
                           GP_11='#6A3D9A'    
                           #,GP_12="black"
                 ),
                 NewGeneAllGroups=c(
                           GP_1='#FF7F00',
                           GP_2='#FFFF99', 
                           GP_3="#B5651D",
                           GP_4='#FDBF6F', 
                           GP_5='#FB9A99',
                           GP_6='#CAB2D6',
                           GP_7='#A6CEE3',
                           GP_8='#1F78B4',
                           GP_9='#33A02C',
                           GP_10='#B2DF8A',
                           GP_11='#6A3D9A',
                           GPC_1="blue",
                           GPC_2="magenta",
                           GPC_3="cyan",
                           GPC_4="orange",
                           GPC_5="red"
                           
                           
                 ),
                NewPrograms = c(GPC_1="blue",
                           GPC_2="magenta",
                           GPC_3="cyan",
                           GPC_4="orange",
                           GPC_5="red"),
                 GuideGroupCombo=c(
                              M3_M3="blue",
                              M3_M5="green", 
                              M5_M5="red"))


"%ni%" = Negate( "%in%" )

computeR2 <- function(response, prediction){
    rss = sum((response - prediction)^2, na.rm = T) ## residual sum of squares
    tss = sum((response - mean(response, na.rm = T))^2) ## total sum of squares
    R2 <- (1- rss/tss)
    return(R2)
}
  
save_pheatmap_pdf <- function(x, filename, width=7, height=7) {
   stopifnot(!missing(x))
   stopifnot(!missing(filename))
   pdf(filename, width=width, height=height)
   grid::grid.newpage()
   grid::grid.draw(x$gtable)
   dev.off()
}


lappend <- function(lst, obj) {
  lst[[length(lst)+1]] <- obj
  return(lst)
}

# Basic function to convert mouse to human gene names
convertMouseGeneList <- function(x){
  
  require("biomaRt")
  human = useMart("ensembl", dataset = "hsapiens_gene_ensembl")
  mouse = useMart("ensembl", dataset = "mmusculus_gene_ensembl")
  
  genesV2 = getLDS(attributes = c("mgi_symbol"), filters = "mgi_symbol", values = x , mart = mouse, attributesL = c("hgnc_symbol"), martL = human, uniqueRows=T)
  humanx <- unique(genesV2[, 2])
  
  # Print the first 6 genes found to the screen
  print(head(humanx))
  return(humanx)
}

# Basic function to convert human to mouse gene names
convertHumanGeneList <- function(x){
  
  require("biomaRt")
  human = useMart("ensembl", dataset = "hsapiens_gene_ensembl")
  mouse = useMart("ensembl", dataset = "mmusculus_gene_ensembl")
  
  genesV2 = getLDS(attributes = c("hgnc_symbol"), filters = "hgnc_symbol", values = x , mart = human, attributesL = c("mgi_symbol"), martL = mouse, uniqueRows=T)
  
  humanx <- unique(genesV2[, 2])
  
  # Print the first 6 genes found to the screen
  print(head(humanx))
  return(humanx)
}


plotDAVIDGORes <- function(backgroundGenes, foregroundGenes, fNamePrefix){
     ensemblBackground <- mapIds(org.Mm.eg.db, keys = backgroundGenes, keytype = "SYMBOL", column= "ENSEMBL")
     ensemblForeground <- mapIds(org.Mm.eg.db, keys = foregroundGenes, keytype = "SYMBOL", column= "ENSEMBL")

     v <- getDAVIDGO( foregroundGenes=ensemblForeground, 
                      backgroundGenes= ensemblBackground,
                      idType="ENSEMBL_GENE_ID",
                      filePath="/home/jovyan/work/analysisSingle/DAVID_DATABASE/",
                      fileNamePrefix=fNamePrefix)
     if(!is.null(v$plotList)){
       if(!is.null(v$plotList$GOTERM_BP_ALL) & v$plotList$GOTERM_BP_ALL != "No plot"){
         print(v$plotList$GOTERM_BP_ALL+ ggtitle(" Biological Process "))
       }

       if(!is.null(v$plotList$GOTERM_CC_ALL) & v$plotList$GOTERM_CC_ALL != "No plot"){
         print(v$plotList$GOTERM_CC_ALL+ ggtitle(" Cellular Component "))
       }

       if(!is.null(v$plotList$GOTERM_MF_ALL) & v$plotList$GOTERM_MF_ALL != "No plot"){
         print(v$plotList$GOTERM_MF_ALL+ggtitle(" Metabolic Process "))
       }    
     } 
}

getOutliers <- function(x){
  qX <- quantile(x)
  IQR = qX[4] - qX[2]
  minLev = qX[2] - 1.5*IQR
  maxLev = qX[4] + 1.5*IQR
  
  return(x[ x < minLev | x > maxLev])
}

getExtremeOutliers <- function(x){
  qX <- quantile(x)
  IQR = qX[4] - qX[2]
  minLev = qX[2] - 3*IQR
  maxLev = qX[4] + 3*IQR
  
  return(x[ x < minLev | x > maxLev])
}

n_fun <- function(x){
  return(data.frame(y = median(x), label = paste0("n = ",length(x))))
}

getJaccardDistanceMatrix <- function(inList){
    tmpDF = data.frame(matrix(0,nrow=length(inList), ncol=length(inList)))
    
    for(i in 1:length(inList)){
        for(j in i:length(inList)){
            tmpDF[i,j] = length(intersect(inList[[i]], inList[[j]] ))/ length(union(inList[[i]], inList[[j]]))
            tmpDF[j,i] = length(intersect(inList[[i]], inList[[j]] ))/ length(union(inList[[i]], inList[[j]]))
        }
    }
    colnames(tmpDF) = names(inList)
    rownames(tmpDF) = names(inList)
    
    return(tmpDF)
}

# --- functions present only in the archived PerturbDecode_v1 copy ---

writePathwayFile <- function(pathwayGenes, fileName, cNames=F){
  maxlen <- max(lengths(pathwayGenes))
  pathwayGenes2 <- lapply(pathwayGenes, function(lst) c(lst, rep(NA, maxlen - length(lst))))

  pathwayGenes.df <- do.call("cbind", lapply(pathwayGenes2, as.data.frame)) 
  colnames(pathwayGenes.df) <- names(pathwayGenes)

  write.table(pathwayGenes.df,  fileName, sep=",", row.names = F, na = " ", quote = F, col.names = cNames)
}
