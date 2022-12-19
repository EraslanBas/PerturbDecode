"%ni%" = Negate( "%in%" )

computeR2 <- function(response, prediction){
    rss = sum((response - prediction)^2, na.rm = T) ## residual sum of squares
    tss = sum((response - mean(response, na.rm = T))^2) ## total sum of squares
    R2 <- (1- rss/tss)
    return(round(R2, digits=2))
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


writePathwayFile <- function(pathwayGenes, fileName, cNames=F){
  maxlen <- max(lengths(pathwayGenes))
  pathwayGenes2 <- lapply(pathwayGenes, function(lst) c(lst, rep(NA, maxlen - length(lst))))

  pathwayGenes.df <- do.call("cbind", lapply(pathwayGenes2, as.data.frame)) 
  colnames(pathwayGenes.df) <- names(pathwayGenes)

  write.table(pathwayGenes.df,  fileName, sep=",", row.names = F, na = " ", quote = F, col.names = cNames)
}