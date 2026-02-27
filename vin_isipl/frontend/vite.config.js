import { defineConfig } from 'vite'
import path from 'path'

export default defineConfig({
	resolve: {
		alias: {
			'@/components/CheckInPanel.vue': path.resolve(
				__dirname,
				'src/components/CheckInPanel.vue'
			),
		},
	},
})