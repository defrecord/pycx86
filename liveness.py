import cparse
from cvisitors import Visitor

class Liveness(Visitor):
    def __init__(self):
        Visitor.__init__(self)
        self.liveness_at_inst = {}
    
    def vTranslationUnit(self, node):
        print "Translation Unit"
        self._visitList(node.nodes)
    
    def vFunctionDefn(self, node):
        print "Function Definition"
        node.body.accept(self)
    
    def vCompoundStatement(self, node):
        print "Compound Statement"
        node.statement_list.accept(self)
        
    def vNodeList(self, node):
        print "Node List"
        rev_list = node.nodes
        rev_list.reverse()
        
        after_live = set([])
        for inst in rev_list:
            # Iterate through the reverse instructions
            W, R = self.visit(inst)
            if not W and not R:
                continue
            
            print W, R
            self.liveness_at_inst[inst] = (after_live - set(W)) | set(R)
            after_live = self.liveness_at_inst[inst]
            
        print self.liveness_at_inst
        
    def vIfStatement(self, node):
        print "If"
        
    def vWhileLoop(self, node):
        print "While"
        
    def vForLoop(self, node):
        print "For"
        
    def vBreakStatement(self, node):
        print "Break"
        
    def vContinueStatement(self, node):
        print "Continue"
        
    def vStringLiteral(self, node):
        print "String"
        
    def vConst(self, node):
        return [None], [None]
        
    def vId(self, node):
        return [node.name]
        
    def vArrayExpression(self, node):
        print "Array"
        
    def vFunctionExpression(self, node):
        print "Function Call"
        
    def vReturnStatement(self, node):
        return [], []
        
    def vBinop(self, node):
        W = []
        R = []
        if (node.op == "="):
            W = [node.left.name]
            nowrite, R = self.visit(node.right)
        else:
            mergedList = self.visit(node.left) + self.visit(node.right)
            R = R + mergedList
            
        # Remove all None values from list
        if (None in R):
            R.remove(None)
        
        return W, R
        
    def vNegative(self, node):
        print "Negative"
        
    def vPointer(self, node):
        print "Pointer"
        
    def vAddrOf(self, node):
        print "Addr Of"