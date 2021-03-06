'''
This HUD script is by G. E. Oscar Toreh

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
'''
import sys
import traceback
import bge
import var
import triggerList
from mathutils import Vector
import gameobjects
import weapons
import triggerHandling

HUD = None
checker = 'HUD Checker'
#HUD_info = None
#reloadTime = 
willUseStatusText = ""

jenisKendaraan = [gameobjects.KX_VehicleObject, gameobjects.KX_AirPlaneObject, gameobjects.KX_TankObject]

minimap_dimensi = 7.0#sementara/default
minimap_jari2 = minimap_dimensi / 2

bgeTextureStats = {bge.texture.SOURCE_ERROR:"bge.texture.SOURCE_ERROR", bge.texture.SOURCE_EMPTY:"bge.texture.SOURCE_EMPTY",
bge.texture.SOURCE_READY:"bge.texture.SOURCE_READY", bge.texture.SOURCE_PLAYING:"bge.texture.SOURCE_PLAYING", bge.texture.SOURCE_STOPPED:"bge.texture.SOURCE_STOPPED"}


def getErrorInfo(ref=None):
	print(' ----------- Error found ------------ ')
	exc_type, exc_obj, exc_tb = sys.exc_info()
	print(sys.exc_info())
	print('pada baris {0}'.format(exc_tb.tb_lineno))
	traceback.print_exc()
	if ref is not None:
		print('referensi:')
		print(ref)
	print(' ------------------------------------ ')
def addHUD():
	bge.logic.addScene('HUD')
	scene = bge.logic.getCurrentScene()
	temp = scene.addObject(checker)
	
def initialize():
	global HUD
	#global HUD_info
	obj = HUD.objects
	#HUD_info = obj['HUD_info']
	
def resizeMinimap(cont):
	own = cont.owner
	scene = bge.logic.getCurrentScene()
	cam = scene.active_camera
	v = cam.getScreenVect(0.5, 0.3)
	y = v.y
	print("minimap y coor = " + str(v))
	own.scaling = Vector([y,y,1])
	
def setMinimap(cont):
	obj = cont.owner
	scene = obj.scene
	# get list of objects in scene
	objList = scene.objects
	kamus = var.globalDict
	
	#obj = objList["Movie"]
	
	# check to see if video texture was created
	if "gambaer" in obj:
		# get the saved video texture
		gambaer = obj["gambaer"]
		
		# update the video
		gambaer.refresh(True)
		
	# create the video texture
	else:
		# get matID for the movie screen
		# my material is named Display 
		matID = bge.texture.materialID(obj, "IMdummy_map_texture")
		#matID = obj.meshes[0].materials[0].getTextureBindcode(0)
		
		# get the texture
		dpTexture = bge.texture.Texture(obj, matID)
		
		map = kamus['map'].split('.')
		# get the name of the movie
		nama = "minimap.png"
		here = bge.logic.expandPath('//')
		map = here + "\\maps\\" + map[0] + "\\" + nama
		print("checking minimap texture from " + str(map) + "...")
		
		# get movie path
		# movie is in same directory as blend
		#movie = bge.logic.expandPath('//' + movieName)
		
		ImageFFmpeg = bge.texture.ImageFFmpeg(map)
		print("status dari ImageFFmpeg-nya ialah : " + str(bgeTextureStats[ImageFFmpeg.status]))
		ada = ImageFFmpeg.valid
		print("image valid is " + str(ada))
		'''
		ImageFFmpeg.refresh()
		print("setelah direfresh")
		print("status dari ImageFFmpeg-nya ialah : " + str(bgeTextureStats[ImageFFmpeg.status]))
		ada = ImageFFmpeg.valid
		print("image valid is " + str(ada))
		ImageFFmpeg.reload(map)
		print("setelah direload")
		print("status dari ImageFFmpeg-nya ialah : " + str(bgeTextureStats[ImageFFmpeg.status]))
		ada = ImageFFmpeg.valid
		print("image valid is " + str(ada))
		ImageFFmpeg.refresh()
		print("setelah direfresh kembali")
		print("status dari ImageFFmpeg-nya ialah : " + str(bgeTextureStats[ImageFFmpeg.status]))
		ada = ImageFFmpeg.valid
		print("image valid is " + str(ada))
		'''
		
		# get movie
		#video.source = bge.texture.VideoFFmpeg(movie)
		dpTexture.source = ImageFFmpeg
		
		# start the video
		dpTexture.refresh(True)
		
		# save dpTexture as an object variable
		obj["gambaer"] = dpTexture
	
def getPlayersPosition(cont):
	own = cont.owner
	#nanti ditambakan scriptnya untuk mengecek posisi2 dari player
	
def spawnMinimap(cont):
	own = cont.owner
	own.position = Vector((0,0,0))
	scene = bge.logic.getCurrentScene()
	print(' ----------------------------------------------- ')
	print('showing up the minimap')
	print(' ----------------------------------------------- ')
	scene.addObject("map plane", own)
	'''
	if cont.sensors['Always'] == 1:
		print(' ----------------------------------------------- ')
		print('showing up the minimap')
		print(' ----------------------------------------------- ')
		scene.addObject("map plane", own)
	'''
	
def deklarasi(cont):
	if 'tim' not in var.scene:
		var.scene['tim'] = 1
	if 'lastSelectedSpawnPoint' not in var.scene:
		var.scene['lastSelectedSpawnPoint'] = None
	if 'playerGUI' not in var.scene:
		var.scene['playerGUI'] = None
	if 'weaponGUI' not in var.scene:
		var.scene['weaponGUI'] = None
	if 'primaryWeaponGUI' not in var.scene:
		var.scene['primaryWeaponGUI'] = None
	if 'addedList' not in var.scene:
		var.scene['addedList'] = []
	if 'tim' not in var.scene:
		var.scene['tim'] = 1
		
def spawnMenuIsOpen(cont):
	var.isSpawnMenuOpened = True
	bge.logic.mouse.visible = True
	if type(var.player) == gameobjects.KX_SoldierObject:
		var.player.disableMouseControl()
def spawnMenuIsClose(cont):
	var.isSpawnMenuOpened = False
	bge.logic.mouse.visible = False
	if type(var.player) == gameobjects.KX_SoldierObject:
		var.player.enableMouseControl()
	
def setTeam(cont):
	own = cont.owner
	s = cont.sensors
	#nanti pake fitur last klik jo supaya nda mo ilang dp view
	if s['over'].positive == 1 and s['klik'].positive == 1:
		var.scene['tim'] = own['tim']
		own.sendMessage("resetSpawner", "", "HUD spawner")
	if var.scene['tim'] == own['tim']:
		for i in own.children:
			i.visible = True
	else:
		for i in own.children:
			i.visible = False
	#print([s['over'].positive == 1 , s['klik'].positive == 1])
	'''
		for i in own.children:
			i.visible = True
		print("{0} has been cliked".format(str(own)))
	elif s['over'].positive == 0 and s['klik'].positive == 1:
		for i in own.children:
			i.visible = False
	'''
	

def setSpawnLoc(cont):
	own = cont.owner
	s = cont.sensors
	if s['over'].positive == 1 and s['klik'].positive == 1:
		var.scene['spawnLoc'] = own['object']
		var.scene['lastSelectedSpawnPoint'] = own
		triggerHandling.onPlayerChooseSpawn(own['object'])
		
	if var.scene['lastSelectedSpawnPoint'] == own:
		own.children['cliked spawnLoc'].visible = True
	else:
		own.children['cliked spawnLoc'].visible = False
	'''
		own.children['cliked spawnLoc'].visible = True
	elif s['over'].positive == 0 and s['klik'].positive == 1:
		own.children['cliked spawnLoc'].visible = False
	'''
	
def addSpawnLoc(cont):
	own = gameobjects.KX_SpawnPoint(cont.owner)
	'''
	if 'spawnLocObjects' not in own:
		own['spawnLocObjects'] = []
	else:
		if own['spawnLocObjects'] != []:
			for i in own['spawnLocObjects']:
				i.endObject()
			own['spawnLocObjects'] = []
	'''
	'''
	if own not in var.spawnLocations:
		var.spawnLocations.append(own)
		var.spawnLocByTeam[own.team].append(own)
	'''
	tim = own.team
	if own not in var.spawnLocByTeam[tim]:
		var.spawnLocByTeam[own.team].append(own)
	'''
	sl = "spawnLocation"
	jari2 = var.mapKonfigurasi['jari2']
	if own['tim'] == var.scene['tim']:
		#print('ok')
		for i in bge.logic.getSceneList():
			if i.name == 'HUD':
				HUD = i
		if HUD != None:
			added = HUD.addObject(sl)
			added.position = Vector((own.position.x / jari2 * minimap_jari2, own.position.y / jari2 * minimap_jari2, 0.2))
			added['pos'] = Vector(own.position)
			own['spawnLocObjects'].append(added)
		else:
			print("On Function addSpawnLoc, HUD not found")
	'''
	
def addTeamHUD(cont):
	scene = bge.logic.getCurrentScene()
	own = cont.owner
	own.position = Vector((-8.41283, 4.59861, 0.0))
	added = scene.addObject('tim A')
	var.scene['addedList'].append(added)
	own.position = Vector((-6.00273, 4.59861, 0.0))
	added = scene.addObject('tim B')
	var.scene['addedList'].append(added)
	
def spawnLocSpawner(cont):
	own = cont.owner
	scene = bge.logic.getCurrentScene()
	if 'addedList' not in var.scene:
		var.scene['addedList'] = []
		
	if 'spawnLocObjects' not in own:
		own['spawnLocObjects'] = []
	else:
		if own['spawnLocObjects'] != []:
			for i in own['spawnLocObjects']:
				i.endObject()
			own['spawnLocObjects'] = []
	
	own.position = Vector((-8.41283, 4.59861, 0.0))
	added = scene.addObject('tim A')
	var.scene['addedList'].append(added)
	own.position = Vector((-6.00273, 4.59861, 0.0))
	added = scene.addObject('tim B')
	var.scene['addedList'].append(added)
	
	sl = "spawnLocation"
	jari2 = var.mapKonfigurasi['jari2']
	if 'tim' not in var.scene:
		var.scene['tim'] = 1
	#print("initializing player object spawner...")
	for h in var.spawnLocByTeam:
		for i in h:
			minimapLoc = Vector((i.position.x / jari2 * minimap_jari2, i.position.y / jari2 * minimap_jari2, 0.2))
			#print("spawnLoc {0} is on location {1} of map and so is should be on {2} at minimap".format(str(i), str(i.position), str(minimapLoc)))
			if i.invalid == False:
				#print("type dari tim i ialah {0} sedangkan type dari tim var scene ialah {1}".format(str(type(i['tim'])), str(type(var.scene['tim']))))
				if i['tim'] == var.scene['tim']:
					#print('ok')
					#own.position = Vector((i.position.x / jari2 * minimap_jari2, i['pos'][1] / jari2 * minimap_jari2, 0.2))
					#own.position = Vector((i.position.x / jari2 * minimap_jari2, i.position.y / jari2 * minimap_jari2, 0.2))
					own.position = minimapLoc
					added = scene.addObject(sl, own)
					#added['pos'] = Vector(i.position)
					added['object'] = i
					var.scene['addedList'].append(added)
					own['spawnLocObjects'].append(added)
					#rotasinya nanti baku iko
				#pilih tim dulu
		
def removeSpawnHUD(cont):
	own = cont.owner
	if 'addedList' in var.scene:
		var.scene['addedList'] = []
		own['spawnLocObjects'] = []
		for i in cont.actuators:
			cont.activate(i)
	
# ----------------- General GUI	----------------- #
def getTeamTickets(cont):
	own = cont.owner
	tiket = KX_TeamTickes(own)
	var.ticketsObject.append(tiket)

def getWillUseStatus(cont):
	own = cont.owner
	global willUseStatusText
	#print('initializing getWillUseStatus')
	if type(own) == bge.types.KX_FontObject:
		own.text = willUseStatusText
			
	#own.text = "None"
	#willUseStatusText
	
def getAmmoSize(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			usage = "{0}"
			if 'usage' in own:
				usage = own['usage']
			if type(var.player) in jenisKendaraan:
				if var.player.currentWeapon != None:
					text = usage.format(str(var.player.currentWeapon.ammo))
					if text != own.text:
						own.text = text
			else:
				if var.player.arms[var.player.currentWeapon] != None:
					text = usage.format(str(var.player.arms[var.player.currentWeapon].ammo))
					if text != own.text:
						own.text = text
	
def getPrimaryAmmoSize(cont):
	own = cont.owner
	#print("ok")
	if var.player != None:
		if var.player.invalid == False:
			usage = "{0}"
			if 'usage' in own:
				usage = own['usage']
			if type(var.player) in jenisKendaraan:
				if var.player.primaryWeapon != None:
					text = usage.format(str(var.player.primaryWeapon.ammo))
					if text != own.text:
						own.text = text
						#can't write
			else:
				if var.player.arms[var.player.primaryWeapon] != None:
					text = usage.format(str(var.player.arms[var.player.primaryWeapon].ammo))
					if text != own.text:
						own.text = text
	
def getMagSize(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			usage = "{0}"
			if 'usage' in own:
				usage = own['usage']
			if type(var.player) in jenisKendaraan:
				if var.player.currentWeapon != None:
					text = usage.format(str(var.player.currentWeapon.mag))
					if text != own.text:
						own.text = text
			else:
				if var.player.arms[var.player.currentWeapon] != None:
					text = usage.format(str(var.player.arms[var.player.currentWeapon].mag))
					if text != own.text:
						own.text = text
	
def getPrimaryMagSize(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			usage = "{0}"
			if 'usage' in own:
				usage = own['usage']
			if type(var.player) in jenisKendaraan:
				if var.player.primaryWeapon != None:
					text = usage.format(str(var.player.primaryWeapon.mag))
					if text != own.text:
						own.text = text
			else:
				if var.player.arms[var.player.primaryWeapon] != None:
					text = usage.format(str(var.player.arms[var.player.primaryWeapon].mag))
					if text != own.text:
						own.text = text
	
def getWeaponName(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			usage = "{0}"
			if 'usage' in own:
				usage = own['usage']
			#print(type(var.player))
			if type(var.player) in jenisKendaraan:
				if var.player.currentWeapon != None:
					text = usage.format(str(var.player.currentWeapon['createWeapon']))
					if text != own.text:
						own.text = text
			else:
				if var.player.arms[var.player.currentWeapon] != None:
					text = usage.format(str(var.player.arms[var.player.currentWeapon].name))
					#if hasattr(var.player, 'arms') == True:
					#	text = usage.format(str(var.player.arms[var.player.currentWeapon].name))
					#else:
					#	text = usage.format(str(var.player.currentWeapon.name))
					if text != own.text:
						own.text = text
	
def getPrimaryWeaponName(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			usage = "{0}"
			if 'usage' in own:
				usage = own['usage']
			#print(type(var.player))
			if type(var.player) in jenisKendaraan:
				if var.player.primaryWeapon != None:
					text = usage.format(str(var.player.primaryWeapon['createPrimaryWeapon']))
					if text != own.text:
						own.text = text
			else:
				if var.player.arms[var.player.primaryWeapon] != None:
					text = usage.format(str(var.player.arms[var.player.primaryWeapon].name))
					#if hasattr(var.player, 'arms') == True:
					#	text = usage.format(str(var.player.arms[var.player.currentWeapon].name))
					#else:
					#	text = usage.format(str(var.player.currentWeapon.name))
					if text != own.text:
						own.text = text
	
def getReloadTime(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			usage = "{0}"
			if 'usage' in own:
				usage = own['usage']
			
			if var.player != None and var.player.invalid == False:
				if type(var.player) in jenisKendaraan:
					if var.player.currentWeapon != None:
						text = usage.format(str(var.player.currentWeapon.reloadTimeLeft))
						if text != own.text:
							own.text = text
				else:
					if var.player.arms[var.player.currentWeapon] != None:
						text = usage.format(str(var.player.arms[var.player.currentWeapon].reloadTimeLeft))
						if text != own.text:
							own.text = text
	
def getPrimaryReloadTime(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			usage = "{0}"
			if 'usage' in own:
				usage = own['usage']
			
			if var.player != None and var.player.invalid == False:
				if type(var.player) in jenisKendaraan:
					if var.player.primaryWeapon != None:
						text = usage.format(str(var.player.primaryWeapon.reloadTimeLeft))
						if text != own.text:
							own.text = text
				else:
					if var.player.arms[var.player.primaryWeapon] != None:
						text = usage.format(str(var.player.arms[var.player.primaryWeapon].reloadTimeLeft))
						if text != own.text:
							own.text = text
	
def getSpeed(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			own.text = str(var.player.worldLinearVelocity.length * 3.6)
		
def getForwardSpeed(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			if "usage" in own:
				own.text = own["usage"].format(str(int(var.player.localLinearVelocity.y * 3.6)))
			else:
				own.text = str(int(var.player.localLinearVelocity.y * 3.6))
		
def getAltitude(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			if "usage" in own:
				own.text = own["usage"].format(str(int(var.player.position.z)))
			else:
				own.text = str(int(var.player.position.z))
		
def getHitPoints(cont):
	own = cont.owner
	if var.player != None:
		if var.player.invalid == False:
			if "usage" in own:
				own.text = own["usage"].format(str(int(var.player.hitPoints)))
			else:
				own.text = str(int(var.player.hitPoints))
				
def setupIndicator(cont):
	own = cont.owner
	if 'type' in own:
		tipe = own['type']
		if tipe == "enemy":
			ei = KX_enemyIndicator(own)
			#nanti perlu mo tambah akang script peresetnya
	
def getPointingRange(cont):
	own = cont.owner
	
def getLockedInfo(cont):
	own = cont.owner
	if 'tik' not in own:
		own['tik'] = 0
	else:
		if var.PCO != None:
			if var.PCO.handle_buffered != None:
				if var.PCO.handle_buffered.status == 1:
					own.visible = True
				else:
					own.visible = False
				#print('cek lock from HUD and it is ' + str(var.PCO.handle_buffered.status))
		#if own['tik'] > own['timeToHide']:
		#	own.visible = False
		#own['tik'] += 1
	
def textGUI(cont):
	own = cont.owner
	
def setUpSingleLockHUD(cont):
	lk = singleLockHUD(cont.owner)
	for act in cont.actuators:
		cont.activate(act)
def runSingleLockHUD(cont):
	cont.owner.run()
	
def setWinnerText(cont):
	KX_WinnerText(cont.owner)
# ----------------------------------------------- #
class simpleObject:
	invalid = True
class KX_WinnerText(bge.types.KX_FontObject):
	hasPoped = False
	teks = 'Team {0} has win the battle'
	def __init__(self, old_owner):
		triggerList.onTicketReachZero.append(self.onSomeTeamLose)
		if 'usage' in self:
			self.teks = self['usage']
	def onSomeTeamLose(self, team):
		if self.hasPoped == False:
			if team == 2:
				t = 'A'
				#self.text = "Team A has win the battle"
				self.text = self.teks.format(t)
			elif team == 1:
				t = 'B'
				#self.text = "Team B has win the battle"
				self.text = self.teks.format(t)
			self.visible = True
			self.hasPoped = True
class KX_TeamTickes(bge.types.KX_FontObject):
	team = 1
	teks = '{0}'
	def __init__(self, old_owner):
		if 'team' in self:
			self.team = self['team']
			if 'usage' in self:
				self.teks = self['usage']
		if self.invalid == False:
			self.text = self.teks.format(str(var.tikets[self.team]))
		triggerList.onPlayerKilled.append(self.triggerUpdateText)
	def triggerUpdateText(self, player, killer, weapon):
		self.updateText()
	def updateText(self):
		self.text = self.teks.format(str(var.tikets[self.team]))
class singleLockHUD(bge.types.KX_GameObject):
	
	def __init__(self, old_owner):
		for i in bge.logic.getSceneList():
			if i.name == "inGame":
				self.inGame = i
		self.camFactorX = self.scene.cameras['cam_of_HUD'].ortho_scale
		self.camFactorY = self.scene.cameras['cam_of_HUD'].ortho_scale * (bge.render.getWindowHeight() / bge.render.getWindowWidth())
	def destroy(self):
		self.endObject()
	def run(self):
		cam = self.inGame.active_camera
		if var.PCO.lockingObject != None and var.PCO.isTracking == True and cam != None:
			if cam.invalid == True or var.PCO.lockingObject.invalid ==  True:
				self.visible = False
				return False
			p = cam.getScreenPosition(var.PCO.lockingObject)
			p = [p[0] - 0.5, p[1] - 0.5]
			self.position.x = p[0] * self.camFactorX
			self.position.y = -p[1] * self.camFactorY
			if var.PCO.lockingObject.invalid == False:
				self.visible = True
				if var.PCO.singleLockStats == "searching":
					self.applyRotation([0, 0, 0.05])
				elif var.PCO.singleLockStats == "locking":
					self.applyRotation([0, 0, 0.05])
				elif var.PCO.singleLockStats == "flareTrack":
					self.applyRotation([0, 0, 0.05])
				elif var.PCO.singleLockStats == "found":
					self.applyRotation([0, 0, 0.05])
				elif var.PCO.singleLockStats == "locked":
					pass
			else:
				self.visible = False
		else:
			self.visible = False

class subIndicator(bge.types.KX_GameObject):
	owner = None
	mimicBy = None
	tick = 0
	idText = None
	def __init__(self, old_owner):
		for i in bge.logic.getSceneList():
			if i.name == "inGame":
				self.inGame = i
		self.window = [bge.render.getWindowWidth(), bge.render.getWindowHeight()]
		#self.windowFactor = [self.window[0]/ ]
		#self.camFactorX = self.scene.cameras['cam_of_HUD'].ortho_scale * (bge.render.getWindowWidth() / bge.render.getWindowHeight())
		self.camFactorX = self.scene.cameras['cam_of_HUD'].ortho_scale
		self.camFactorY = self.scene.cameras['cam_of_HUD'].ortho_scale * (bge.render.getWindowHeight() / bge.render.getWindowWidth())
		
		#get child data
		for i in self.childrenRecursive:
			if 'getID' in i:
				self.idText = i
		#--------------
	def run(self):
		#cek = [self.mimicBy, var.objectsInView]
		#print(cek)
		if self.tick > 0:
			if self.mimicBy not in var.objectsInView:
				#print("got deleted")
				print('nope object sub indicator has been deleted because mimicBy not in var.objectsInView')
				del self.owner.daftar[self.mimicBy]
				self.endObject()
				return False
			else:
				if self.mimicBy == None:
					print('nope object sub indicator has been deleted because mimicBy is None')
					del self.owner.daftar[self.mimicBy]
					self.endObject()
					return False
				else:
					if self.mimicBy.invalid == False:
						#print('oj')
						if self.idText != None:
							if self.mimicBy.owner != None:
								if self.mimicBy.owner.invalid == False:
									if self.mimicBy.owner.nick != None:
										self.idText.text = str(self.mimicBy.owner.nick)
									else:
										self.idText.text = str(id(self.mimicBy))
							else:
								self.idText.text = str(id(self.mimicBy))
						cam = self.inGame.active_camera
						if cam != None:
							p = cam.getScreenPosition(self.mimicBy)
							v = cam.parent.getVectTo(self.mimicBy)
							if v[2][1] < 0:
								self.visible = False
							else:
								self.visible = True
								p = [p[0] - 0.5, p[1] - 0.5]
								self.position.x = p[0] * self.camFactorX
								self.position.y = -p[1] * self.camFactorY
								self.position.z = 0.0
								#print(self.position)
					else:
						print('nope object sub indicator has been deleted')
						self.endObject()
						return False
		self.tick += 1
class KX_enemyIndicator(bge.types.KX_GameObject):
	daftar = {}
	daftarHitObject = []
	def __init__(self, old_owner):
		triggerList.onRadarUpdate.append(self.onViewUpdate)
	def onViewUpdate(self, daftarHitObject):
		#algoritma untuk mengupdate indicatornya
		#print("executing on view update")
		#print("dp daftar = " + str(self.daftarHitObject))
		for obj in daftarHitObject:
			if hasattr(obj, 'owner'):
				if obj.owner != None:
					if obj.owner.team != var.PCO.team:
						#addSubIndikator
						#print("updating viewList object")
						if self.invalid == False:
							if 'shownAs' in self:
								if obj not in self.daftar:
									shownAs = self['shownAs']
									added = self.scene.addObject(shownAs)
									added = subIndicator(added)
									added.owner = self
									added.mimicBy = obj
									self.daftar[obj] = added
									#self.daftar[obj].run()
								else:
									#self.daftar[obj].run()
									#print(var.objectsInView)
									pass
						else:
							print("some indicator object is invalid")
							
		pass
'''
class KX_useIndikator(bge.types.KX_FontObject):
	def __init__(self, old_owner):
		print("initializing " + str(self))
		self.text = ""
	def run(self):
		pass

class KX_reloadGUI(bge.types.KX_FontObject):
	def __init__(self, old_owner):
		pass
	def run(self):
		pass

class KX_GUI(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self.runList = []
		#print("initializing GUI of " + str(self))
		for child in self.childrenRecursive:
			if type(child) == bge.types.KX_FontObject:
				if child['ref'] == "getWillUseStatus":
					#print("adding getWillUseStatus for GUI" + str(self))
					obj = KX_useIndikator(child)
					self.runList.append(obj)
	def run(self):
		for i in self.runList:
			i.run()
'''

# ----------------- Set Up GUI	----------------- #
def setGUI(cont):
	own = cont.owner
	#print("setting up GUI of object " + str(own))
	#KX_GUI(own)
	
def runGUI(cont):
	own = cont.owner
	own.run()
	
'''
def hudSpawnerSetUp(cont):
	own = cont,owner
	own['useByPlayer'] = None
'''
	
def getPlayerGUI(cont):
	own = cont.owner
	scene = own.scene
	if var.player != None and var.player.invalid == False:
		if var.player.guiIndex != None:
			if type(var.player) in jenisKendaraan:
				if var.scene['playerGUI'] == None:
					scene.addObject(var.player.guiIndex)
					var.scene['playerGUI'] = var.player.guiIndex
				else:
					if var.player.guiIndex != var.scene['playerGUI']:
						scene.objects[var.scene['playerGUI']].endObject()
						scene.addObject(var.player.guiIndex)
						var.scene['playerGUI'] = var.player.guiIndex
			else:
				if var.scene['playerGUI'] == None:
					scene.addObject(var.player.guiIndex)
					var.scene['playerGUI'] = var.player.guiIndex
				else:
					if var.player.guiIndex != var.scene['playerGUI']:
						scene.objects[var.scene['playerGUI']].endObject()
						scene.addObject(var.player.guiIndex)
						var.scene['playerGUI'] = var.player.guiIndex
	else:
		if 'playerGUI' in var.scene:
			if var.scene['playerGUI'] != None:
				scene.objects[var.scene['playerGUI']].endObject()
				print('disabling playerGUI GUI of {0} '.format(var.scene['playerGUI']))
				var.scene['playerGUI'] = None
	
def getWeaponGUI(cont):
	own = cont.owner
	scene = own.scene
	if var.player != None and var.player.invalid == False:
		if type(var.player) in jenisKendaraan:
			#print("player is in vehicle")
			if var.player.currentWeapon!= None:
				#print(var.player.currentWeapon.name)
				if var.player.currentWeapon.weaponGUI != None:
					#print("vehicle gui is not none")
					#print([var.player.currentWeapon.weaponGUI, var.scene['weaponGUI']])
					if var.player.currentWeapon.weaponGUI != var.scene['weaponGUI']:
						if var.scene['weaponGUI'] == None:
							scene.addObject(var.player.currentWeapon.weaponGUI)
							var.scene['weaponGUI'] = var.player.currentWeapon.weaponGUI
						else:
							if var.scene['weaponGUI'] != None:
								if var.scene['weaponGUI'] in scene.objects:
									scene.objects[var.scene['weaponGUI']].endObject()
									#print("dp gui ialah = " + var.player.currentWeapon.weaponGUI)
									scene.addObject(var.player.currentWeapon.weaponGUI)
									var.scene['weaponGUI'] = var.player.currentWeapon.weaponGUI
				else:
					if var.scene['weaponGUI'] != None:
						if scene.objects[var.scene['weaponGUI']] != None:
							scene.objects[var.scene['weaponGUI']].endObject()
							var.scene['weaponGUI'] = None
			#primaryWeapon section
			if var.player.primaryWeapon!= None:
				#print(var.player.primaryWeapon.name)
				if var.player.primaryWeapon.weaponGUI != None:
					#print("vehicle gui is not none")
					#print([var.player.primaryWeapon.weaponGUI, var.scene['weaponGUI']])
					if var.player.primaryWeapon.weaponGUI != var.scene['primaryWeaponGUI']:
						if var.scene['primaryWeaponGUI'] == None:
							scene.addObject(var.player.primaryWeapon.weaponGUI)
							var.scene['primaryWeaponGUI'] = var.player.primaryWeapon.weaponGUI
						else:
							if var.scene['primaryWeaponGUI'] != None:
								if var.scene['primaryWeaponGUI'] in scene.objects:
									scene.objects[var.scene['primaryWeaponGUI']].endObject()
									#print("dp gui ialah = " + var.player.primaryWeapon.weaponGUI)
									scene.addObject(var.player.primaryWeapon.weaponGUI)
									var.scene['primaryWeaponGUI'] = var.player.primaryWeapon.weaponGUI
				else:
					if var.scene['primaryWeaponGUI'] != None:
						if scene.objects[var.scene['primaryWeaponGUI']] != None:
							scene.objects[var.scene['primaryWeaponGUI']].endObject()
							var.scene['primaryWeaponGUI'] = None
			#---------------------
		else:
			if var.player.arms[var.player.currentWeapon] != None:
				if var.player.arms[var.player.currentWeapon].weaponGUI != None:
					if var.player.arms[var.player.currentWeapon].weaponGUI != var.scene['weaponGUI']:
						if var.scene['weaponGUI'] == None:
							scene.addObject(var.player.arms[var.player.currentWeapon].weaponGUI)
							var.scene['weaponGUI'] = var.player.arms[var.player.currentWeapon].weaponGUI
						else:
							scene.objects[var.scene['weaponGUI']].endObject()
							scene.addObject(var.player.arms[var.player.currentWeapon].weaponGUI)
							var.scene['weaponGUI'] = var.player.arms[var.player.currentWeapon].weaponGUI
				else:
					if var.player.arms[var.player.currentWeapon].weaponGUI != var.scene['weaponGUI']:
						scene.objects[var.scene['weaponGUI']].endObject()
						var.scene['weaponGUI'] = None
	else:
		#disable weapon GUI
		if 'weaponGUI' in var.scene:
			if var.scene['weaponGUI'] != None:
				scene.objects[var.scene['weaponGUI']].endObject()
				print('disabling weapon GUI of {0} '.format(var.scene['weaponGUI']))
				var.scene['weaponGUI'] = None
		if 'primaryWeaponGUI' in var.scene:
			if var.scene['primaryWeaponGUI'] != None:
				scene.objects[var.scene['primaryWeaponGUI']].endObject()
				print('disabling weapon GUI of {0} '.format(var.scene['primaryWeaponGUI']))
				var.scene['primaryWeaponGUI'] = None
def removePGUI(cont):
	for i in bge.logic.getSceneList():
		if i.name == 'HUD':
			#scene = bge.logic.getCurrentScene()
			scene = i
			if var.scene['playerGUI'] != None:
				obj = scene.objects[var.scene['playerGUI']]
				obj.endObject()
				var.scene['playerGUI'] = None
def removeWGUI(cont):
	for i in bge.logic.getSceneList():
		if i.name == 'HUD':
			#scene = bge.logic.getCurrentScene()
			scene = i
			if var.scene['weaponGUI'] != None:
				obj = scene.objects[var.scene['weaponGUI']]
				obj.endObject()
				var.scene['weaponGUI'] = None
def removeGUI(GUI, dari):
	for i in bge.logic.getSceneList():
		if i.name == 'HUD':
			#scene = bge.logic.getCurrentScene()
			scene = i
			if var.scene[dari] != None:
				obj = scene.objects[GUI]
				obj.endObject()
				var.scene[dari] = None
	
def updateGUI(cont):
	own = cont.owner
# ----------------------------------------------- #

# ----------------- Vehicle GUI	----------------- #

# ----------------------------------------------- #

def delGUIHUD():
	own = cont.owner
	#reset HUD like a ammo left, mag left, weapon name, HP Bar, etc
	
def setGUIHUD(cont):
	own = cont.owner
	#konvert pixel ke desimal untuk mendapatkan nilai world dari x dan y
	#adding HUD like a ammo left, mag left, weapon name, HP Bar, etc <--- has already replaced by simple linked HUD files

def cekSpawnLokForJoinText(cont):
	own = cont.owner
	if 'spawnLoc' in var.scene:
		#var.scene['spawnLoc']
		own.text = 'Click here to join the battle'
	
def spawnPlayer(cont):
	#playerSpawner
	if 'spawnLoc' in var.scene:
		if var.player != True:
			jari2 = var.mapKonfigurasi['jari2']
			lok = var.scene['spawnLoc']
			for scene in bge.logic.getSceneList():
				if scene.name == "inGame":
					kamus = var.globalDict
					#ps = scene.objects['playerSpawner']
					#ps.position = lok.position
					#ps.worldOrientation = lok.worldOrientation
					#player = scene.addObject("Soldier", ps)
					#var.player = gameobjects.KX_SoldierObject(player)
					player = scene.addObject(var.spawnAs, lok)
					#var.player = player
					#var.player = gameobjects.setPlayerVehicle(player)
					try:
						var.player = gameobjects.KX_AirPlaneObject(player)
						weapons.setWeapons(var.player)
					except:
						getErrorInfo()
						bge.logic.endGame()
					#var.player.team = var.scene['tim']
					var.PCO.gameObject = var.player
					var.player.owner = var.PCO
					var.PCO.team = var.scene['tim']
					triggerHandling.onPlayerSpawn(var.PCO, lok)
					print("player has beend added with name {0} and type {1}".format(var.player.name, str(type(var.player))))
					scene.addObject('setCamposObject')
					print('setCamposObject has been added')
					#kamus['objek'][var.player] = {'useBy':'player'}
					bge.logic.mouse.visible = False
					'''
					print(" ---------------------------- ")
					print("checking data in kamus...")
					for i in kamus['objek']:
						tipe = type(i)
						print("objek {0} dengan tipe {1}".format(str(i), str(tipe)))
					print(" ---------------------------- ")
					'''
					break
	
'''
def printReloadTime(t):
	global reloadTime
	if type(reloadTime) == bge.types.KX_FontObject:
		reloadTime.text = "Reload Time : " + str(t)
'''
	
def findHUD(cont):
	own = cont.owner
	scenes = bge.logic.getSceneList()
	global HUD
	for i in scenes:
		if i.name == 'HUD':
			HUD = i
	if HUD is None:
		print('requesting HUD data is timeout')
		print('isi daftar scene ialah {0}'.format(str(scenes)))
	else:
		initialize()
		own.endObject()
		
def end():
	global HUD
	#global HUD_info
	for i in HUD.objects:
		i.removeParent()
	for i in HUD.objects:
		i.endObjects()
	'''
	'''
	HUD.end()
	HUD = None
	#HUD_info = None