from random import randint
from time import sleep


class Graph:
	def __init__(self, vertices):
		self.graph = []
		if isinstance(vertices, int):
			self.V = vertices
		else:
			self.add_by_file(vertices)
		self.changed = False

	def add_edge(self, u, v, w):
		self.graph.append([u, v, w])

	def add_by_file(self, file_name):
		file = open(file_name, 'r')
		lines = file.readlines()
		for i in range(len(lines)):
			lines[i] = lines[i].replace('\n', '')
		self.V = int(lines[0])
		del(lines[0])
		for x in lines:
			temp = x.split(',')
			self.add_edge(self.to_num(temp[0]), self.to_num(temp[1]), int(temp[2]))
			self.add_edge(self.to_num(temp[1]), self.to_num(temp[0]), int(temp[2]))

	@staticmethod
	def to_num(letter):
		return ord(letter) - 65

	@staticmethod
	def to_letter(num):
		return chr(num + 65)

	def print_arr(self, dist):
		print("Vertex   Distance from Source")
		for i in range(self.V):
			print("{} \t\t {}".format(self.to_letter(i), dist[i]))

	def bellman_ford(self, source):
		distance = [float("Inf")] * self.V
		distance[source] = 0
		previous = [None] * self.V
		previous[source] = source

		for i in range(self.V - 1):
			for u, v, w in self.graph:
				if distance[u] != float("Inf") and distance[u] + w < distance[v]:
					distance[v] = distance[u] + w
					previous[v] = u

		for u, v, w in self.graph:
			if distance[u] != float("Inf") and distance[u] + w < distance[v]:
				print("Graph contains negative weight cycle")
				return

		return distance, previous

	def get_grid(self):
		distances = '    '
		for i in range(self.V):
			distances += '{0:3}'.format(self.to_letter(i))
		distances += '\n\n'
		path = distances
		for i in range(self.V):
			distances += "{0:3}".format(self.to_letter(i))
			path += "{0:5}".format(self.to_letter(i))
			nums, previous_nodes = self.bellman_ford(i)
			for num in nums:
				distances = distances + '{0:3}'.format(num)
			distances += '\n'
			for node in previous_nodes:
				path = path + '{0:3}'.format(self.to_letter(node))
			path += '\n'
		print('Distance Chart:', '\n', distances)
		print('Shortest Path Chart:', '\n', path)

	def run(self):
		print('Program is now running\nPress ctrl + c to exit')
		sleep(2)
		self.get_grid()

		while True:
			try:
				sleep(1)
				if self.changed:
					print('Distances have changed')
					self.get_grid()
				rand = randint(0, 10)
				if rand < 3:
					self.changed = True
					to_change = randint(0, self.V - 1)
					add_or_subtract = randint(0, 1)
					if add_or_subtract == 1 and self.graph[to_change][2] < 0:
						self.graph[to_change][2] -= 1
					else:
						self.graph[to_change][2] += 1
				else:
					self.changed = False
			except (KeyboardInterrupt, EOFError):
				print('\n\nExiting now. Have a nice day')
				exit(0)


if __name__ == '__main__':
	g = Graph('graph.txt')
	g.run()
