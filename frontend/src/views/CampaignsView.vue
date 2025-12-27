<script setup>
import { ref, onMounted, computed } from 'vue'
import { crmService } from '../services/api'

const campaigns = ref([])
const deals = ref([])
const loading = ref(true)
const dialog = ref(false)
const viewMode = ref('card')
const search = ref('')
const editedIndex = ref(-1)
const editedItem = ref({
  name: '',
  campaign_type: 'email',
  status: 'planning',
  budget: 0,
  description: '',
  start_date: null,
  end_date: null,
  deal: null
})

const defaultItem = {
  name: '',
  campaign_type: 'email',
  status: 'planning',
  budget: 0,
  description: '',
  start_date: null,
  end_date: null,
  deal: null
}

const headers = [
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Type', key: 'campaign_type', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Budget', key: 'budget', sortable: true },
  { title: 'Start Date', key: 'start_date', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
]

const typeChoices = [
  { title: 'Email', value: 'email' },
  { title: 'Social Media', value: 'social' },
  { title: 'Event/Trade Show', value: 'event' },
  { title: 'Paid Search/Ads', value: 'ads' }
]

const statusChoices = [
  { title: 'Planning', value: 'planning' },
  { title: 'Active', value: 'active' },
  { title: 'Completed', value: 'completed' },
  { title: 'Cancelled', value: 'cancelled' }
]

const filteredCampaigns = computed(() => {
  if (!search.value) return campaigns.value
  const searchLower = search.value.toLowerCase()
  return campaigns.value.filter(campaign =>
    campaign.name && campaign.name.toLowerCase().includes(searchLower) ||
    campaign.campaign_type && campaign.campaign_type.toLowerCase().includes(searchLower) ||
    campaign.status && campaign.status.toLowerCase().includes(searchLower)
  )
})

onMounted(async () => {
  await Promise.all([loadCampaigns(), loadDeals()])
})

const loadCampaigns = async () => {
  loading.value = true
  try {
    campaigns.value = await crmService.getCampaigns()
  } catch (error) {
    console.error('Failed to load campaigns:', error)
  } finally {
    loading.value = false
  }
}

const loadDeals = async () => {
  try {
    deals.value = await crmService.getDeals()
  } catch (error) {
    console.error('Failed to load deals:', error)
  }
}

const editItem = (item) => {
  editedIndex.value = campaigns.value.indexOf(item)
  editedItem.value = Object.assign({}, item)
  dialog.value = true
}

const deleteItem = async (item) => {
  if (confirm('Are you sure you want to delete this campaign?')) {
    try {
      await crmService.deleteCampaign(item.id)
      await loadCampaigns()
    } catch (error) {
      console.error('Failed to delete campaign:', error)
    }
  }
}

const close = () => {
  dialog.value = false
  setTimeout(() => {
    editedItem.value = Object.assign({}, defaultItem)
    editedIndex.value = -1
  }, 300)
}

const save = async () => {
  try {
    if (editedIndex.value > -1) {
      await crmService.updateCampaign(editedItem.value.id, editedItem.value)
    } else {
      await crmService.createCampaign(editedItem.value)
    }
    await loadCampaigns()
    close()
  } catch (error) {
    console.error('Failed to save campaign:', error)
  }
}

const getInitials = (name) => {
  return name ? name.substring(0, 2).toUpperCase() : 'CA'
}

const getAvatarColor = (index) => {
  const colors = ['primary', 'secondary', 'success', 'info', 'warning', 'purple', 'pink', 'indigo', 'teal', 'orange']
  return colors[index % colors.length]
}

const getStatusColor = (status) => {
  const colors = {
    planning: 'warning',
    active: 'success',
    completed: 'info',
    cancelled: 'error'
  }
  return colors[status] || 'grey'
}

const getTypeIcon = (type) => {
  const icons = {
    email: 'mdi-email',
    social: 'mdi-share-variant',
    event: 'mdi-calendar-star',
    ads: 'mdi-bullhorn'
  }
  return icons[type] || 'mdi-bullhorn'
}
</script>

<template>
  <v-container fluid class="pa-6">
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-6 flex-wrap gap-3">
          <div>
            <h1 class="text-h3 font-weight-bold text-navy mb-2">Campaigns</h1>
            <p class="text-h6 text-grey-darken-1">Manage your marketing campaigns</p>
          </div>
          <v-btn color="primary" size="large" prepend-icon="mdi-plus" @click="dialog = true" elevation="2">
            Add Campaign
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="mb-4">
          <v-card-text class="pa-4">
            <div class="d-flex align-center gap-3 flex-wrap">
              <v-text-field
                v-model="search"
                prepend-inner-icon="mdi-magnify"
                label="Search campaigns..."
                variant="outlined"
                density="compact"
                hide-details
                clearable
                class="flex-grow-1"
                style="max-width: 400px;"
              ></v-text-field>
              <v-spacer></v-spacer>
              <v-btn-toggle v-model="viewMode" mandatory variant="outlined" divided density="compact">
                <v-btn value="card" size="small"><v-icon>mdi-view-grid</v-icon></v-btn>
                <v-btn value="table" size="small"><v-icon>mdi-view-list</v-icon></v-btn>
              </v-btn-toggle>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col cols="12" class="text-center py-12">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else-if="viewMode === 'card'">
      <v-col v-for="(campaign, index) in filteredCampaigns" :key="campaign.id" cols="12" sm="6" md="4" lg="3">
        <v-card elevation="3" class="campaign-card h-100" hover>
          <v-card-text class="pa-4 text-center">
            <v-avatar :color="getAvatarColor(index)" size="64" class="mb-3">
              <v-icon color="white" size="32">{{ getTypeIcon(campaign.campaign_type) }}</v-icon>
            </v-avatar>
            <h3 class="text-h6 font-weight-bold mb-1">{{ campaign.name }}</h3>
            <v-chip :color="getStatusColor(campaign.status)" size="small" class="mb-3">
              {{ campaign.status }}
            </v-chip>
            
            <v-divider class="my-3"></v-divider>
            
            <div class="campaign-details text-left">
              <div class="d-flex align-center mb-2">
                <v-icon size="small" class="mr-2" color="grey-darken-1">mdi-cash</v-icon>
                <span class="text-caption font-weight-medium">${{ campaign.budget }}</span>
              </div>
              <div class="d-flex align-center mb-2" v-if="campaign.start_date">
                <v-icon size="small" class="mr-2" color="grey-darken-1">mdi-calendar-start</v-icon>
                <span class="text-caption">{{ campaign.start_date }}</span>
              </div>
              <div class="d-flex align-center" v-if="campaign.end_date">
                <v-icon size="small" class="mr-2" color="grey-darken-1">mdi-calendar-end</v-icon>
                <span class="text-caption">{{ campaign.end_date }}</span>
              </div>
            </div>
          </v-card-text>
          <v-card-actions class="pa-3 pt-0">
            <v-btn size="small" variant="text" color="primary" prepend-icon="mdi-pencil" @click="editItem(campaign)">
              Edit
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn size="small" variant="text" color="error" icon="mdi-delete" @click="deleteItem(campaign)"></v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col v-if="filteredCampaigns.length === 0" cols="12">
        <v-card elevation="2" class="pa-12">
          <div class="text-center">
            <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-bullhorn-outline</v-icon>
            <h3 class="text-h5 mb-2 text-grey-darken-1">No campaigns found</h3>
            <p class="text-body-2 text-grey mb-4">
              {{ search ? 'Try adjusting your search' : 'Get started by creating your first campaign' }}
            </p>
            <v-btn v-if="!search" color="primary" @click="dialog = true" prepend-icon="mdi-plus">Add Campaign</v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col cols="12">
        <v-card elevation="3">
          <v-data-table :headers="headers" :items="filteredCampaigns" :loading="loading" items-per-page="15">
            <template v-slot:item.name="{ item, index }">
              <div class="d-flex align-center py-2">
                <v-avatar :color="getAvatarColor(index)" size="36" class="mr-3">
                  <v-icon color="white" size="20">{{ getTypeIcon(item.campaign_type) }}</v-icon>
                </v-avatar>
                <span class="font-weight-medium">{{ item.name }}</span>
              </div>
            </template>
            <template v-slot:item.status="{ item }">
              <v-chip :color="getStatusColor(item.status)" size="small">
                {{ item.status }}
              </v-chip>
            </template>
            <template v-slot:item.budget="{ item }">
              <span class="font-weight-medium">${{ item.budget }}</span>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-icon size="small" class="mr-2" @click="editItem(item)" color="primary">mdi-pencil</v-icon>
              <v-icon size="small" @click="deleteItem(item)" color="error">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="700px" persistent>
      <v-card>
        <v-card-title class="pa-4 bg-grey-lighten-4">
          <div class="d-flex align-center">
            <v-icon class="mr-2" color="primary">{{ editedIndex === -1 ? 'mdi-bullhorn-variant' : 'mdi-pencil' }}</v-icon>
            <span class="text-h6 font-weight-bold">{{ editedIndex === -1 ? 'New Campaign' : 'Edit Campaign' }}</span>
          </div>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-6">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="editedItem.name" label="Campaign Name *" variant="outlined" color="primary" prepend-inner-icon="mdi-bullhorn" required></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedItem.campaign_type"
                  :items="typeChoices"
                  label="Campaign Type"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-tag"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedItem.status"
                  :items="statusChoices"
                  label="Status"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-flag"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field v-model="editedItem.budget" label="Budget" type="number" variant="outlined" color="primary" prepend-inner-icon="mdi-cash" prefix="$"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="editedItem.deal"
                  :items="deals"
                  item-title="title"
                  item-value="id"
                  label="Associated Deal"
                  variant="outlined"
                  color="primary"
                  prepend-inner-icon="mdi-handshake"
                  clearable
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field v-model="editedItem.start_date" label="Start Date" type="date" variant="outlined" color="primary" prepend-inner-icon="mdi-calendar-start"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field v-model="editedItem.end_date" label="End Date" type="date" variant="outlined" color="primary" prepend-inner-icon="mdi-calendar-end"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea v-model="editedItem.description" label="Description" variant="outlined" color="primary" prepend-inner-icon="mdi-text" rows="3"></v-textarea>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="close" size="large">Cancel</v-btn>
          <v-btn color="primary" variant="flat" @click="save" size="large" prepend-icon="mdi-content-save">Save Campaign</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.campaign-card {
  transition: all 0.3s ease;
  border-top: 4px solid transparent;
}

.campaign-card:hover {
  transform: translateY(-4px);
  border-top-color: rgb(var(--v-theme-primary));
}

.campaign-details {
  min-height: 72px;
}

.text-navy {
  color: #1a237e;
}
</style>