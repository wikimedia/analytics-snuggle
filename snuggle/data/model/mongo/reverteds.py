from snuggle.data import types

class Reverteds:
	
	def __init__(self, db):
		self.db = db
	
	def __contains__(self, pageId):
		return self.db.reverteds.find({'revision.page._id': pageId}).count() > 0
	
	def new(self, reverted):
		return self.db.reverteds.insert(reverted.deflate())
	
	def get(self, pageId):
		for json in self.db.users.find({'revision.page.id': pageId}):
			yield Reverted(self.db, json)
		
	
	

class Reverted:
	
	PROCESS_LIMIT = 5
	
	def __init__(self, db, json):
		self.db        = db
		self.id        = json['_id']
		self.sha1      = json['sha1']
		self.processed = json['processed']
		self.revision  = types.Revision.inflate(json['revision'])
		self.history   = json['history']
	
	def complete():
		return self.processed >= self.PROCESS_LIMIT or self.revert != None
	
	def process(revision):
		if revision.sha1 in self.history and revision.sha1 != self.sha1:
			self.revert = revision
			self.db.users.update(
				{'_id': self.revision.user.id},
				{
					'$set': {
						'revisions.%s.revert' % revision.id: revision.deflate()
					}
				}
			)
			self.delete()
		else:
			self.processed += 1
			
			if self.processed < self.PROCESS_LIMIT:
				self.db.reverteds.update(
					{'_id': self.id},
					{'$set': {'processed': self.processed}},
					safe=True
				)
			else:
				self.delete()
		
	def delete(self):
		self.db.reverteds.remove({'_id': self.id})
			
			
		
		
