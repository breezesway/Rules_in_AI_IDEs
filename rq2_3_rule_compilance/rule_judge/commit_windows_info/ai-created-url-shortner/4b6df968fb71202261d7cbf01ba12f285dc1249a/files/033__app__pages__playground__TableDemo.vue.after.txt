<script setup lang="ts">
definePageMeta({
  title: "Table Demo",
  description: "Data table component with sorting and selection",
});

const invoices = [
  {
    id: "INV001",
    status: "Paid",
    method: "Credit Card",
    amount: "$250.00",
  },
  {
    id: "INV002",
    status: "Pending",
    method: "PayPal",
    amount: "$150.00",
  },
  {
    id: "INV003",
    status: "Unpaid",
    method: "Bank Transfer",
    amount: "$350.00",
  },
  {
    id: "INV004",
    status: "Paid",
    method: "Credit Card",
    amount: "$450.00",
  },
  {
    id: "INV005",
    status: "Paid",
    method: "PayPal",
    amount: "$550.00",
  },
  {
    id: "INV006",
    status: "Pending",
    method: "Bank Transfer",
    amount: "$200.00",
  },
  {
    id: "INV007",
    status: "Unpaid",
    method: "Credit Card",
    amount: "$300.00",
  },
];

const users = [
  {
    id: 1,
    name: "John Doe",
    email: "john@example.com",
    role: "Admin",
    status: "Active",
  },
  {
    id: 2,
    name: "Jane Smith",
    email: "jane@example.com",
    role: "Editor",
    status: "Active",
  },
  {
    id: 3,
    name: "Bob Johnson",
    email: "bob@example.com",
    role: "Viewer",
    status: "Inactive",
  },
  {
    id: 4,
    name: "Alice Brown",
    email: "alice@example.com",
    role: "Editor",
    status: "Active",
  },
];

const getStatusColor = (status: string) => {
  switch (status) {
    case "Paid":
    case "Active":
      return "bg-green-100 text-green-800 hover:bg-green-100 dark:bg-green-900 dark:text-green-300";
    case "Pending":
      return "bg-yellow-100 text-yellow-800 hover:bg-yellow-100 dark:bg-yellow-900 dark:text-yellow-300";
    case "Unpaid":
    case "Inactive":
      return "bg-red-100 text-red-800 hover:bg-red-100 dark:bg-red-900 dark:text-red-300";
    default:
      return "";
  }
};
</script>

<template>
  <div class="max-w-6xl mx-auto space-y-8">
    <div>
      <h1 class="text-3xl font-bold tracking-tight">Table</h1>
      <p class="text-muted-foreground mt-2">
        A responsive table component for displaying data.
      </p>
    </div>

    <!-- Basic Table -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Basic Table</h2>
      <div class="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead class="w-[100px]">Invoice</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Method</TableHead>
              <TableHead class="text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="invoice in invoices" :key="invoice.id">
              <TableCell class="font-medium">{{ invoice.id }}</TableCell>
              <TableCell>
                <Badge :class="getStatusColor(invoice.status)">
                  {{ invoice.status }}
                </Badge>
              </TableCell>
              <TableCell>{{ invoice.method }}</TableCell>
              <TableCell class="text-right">{{ invoice.amount }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>

    <!-- Table with Selection -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Table with Selection</h2>
      <div class="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead class="w-[50px]">
                <Checkbox />
              </TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Role</TableHead>
              <TableHead>Status</TableHead>
              <TableHead class="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="user in users" :key="user.id">
              <TableCell>
                <Checkbox />
              </TableCell>
              <TableCell class="font-medium">{{ user.name }}</TableCell>
              <TableCell>{{ user.email }}</TableCell>
              <TableCell>
                <Badge variant="outline">{{ user.role }}</Badge>
              </TableCell>
              <TableCell>
                <Badge :class="getStatusColor(user.status)">
                  {{ user.status }}
                </Badge>
              </TableCell>
              <TableCell class="text-right">
                <div class="flex justify-end gap-2">
                  <Button variant="ghost" size="sm">Edit</Button>
                  <Button variant="ghost" size="sm" class="text-destructive"
                    >Delete</Button
                  >
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>

    <!-- Table with Caption and Footer -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Table with Caption and Footer</h2>
      <div class="rounded-md border">
        <Table>
          <TableCaption>A list of your recent invoices.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead class="w-[100px]">Invoice</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Method</TableHead>
              <TableHead class="text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow v-for="invoice in invoices.slice(0, 5)" :key="invoice.id">
              <TableCell class="font-medium">{{ invoice.id }}</TableCell>
              <TableCell>
                <Badge :class="getStatusColor(invoice.status)">
                  {{ invoice.status }}
                </Badge>
              </TableCell>
              <TableCell>{{ invoice.method }}</TableCell>
              <TableCell class="text-right">{{ invoice.amount }}</TableCell>
            </TableRow>
          </TableBody>
          <TableFooter>
            <TableRow>
              <TableCell colspan="3">Total</TableCell>
              <TableCell class="text-right">$1,750.00</TableCell>
            </TableRow>
          </TableFooter>
        </Table>
      </div>
    </div>

    <!-- Compact Table -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Compact Table</h2>
      <div class="rounded-md border">
        <Table class="text-sm">
          <TableHeader>
            <TableRow>
              <TableHead class="h-8">Product</TableHead>
              <TableHead class="h-8">SKU</TableHead>
              <TableHead class="h-8">Stock</TableHead>
              <TableHead class="h-8 text-right">Price</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell class="h-8 font-medium">Laptop</TableCell>
              <TableCell class="h-8">LAP-001</TableCell>
              <TableCell class="h-8">23</TableCell>
              <TableCell class="h-8 text-right">$999.00</TableCell>
            </TableRow>
            <TableRow>
              <TableCell class="h-8 font-medium">Mouse</TableCell>
              <TableCell class="h-8">MOU-001</TableCell>
              <TableCell class="h-8">156</TableCell>
              <TableCell class="h-8 text-right">$29.99</TableCell>
            </TableRow>
            <TableRow>
              <TableCell class="h-8 font-medium">Keyboard</TableCell>
              <TableCell class="h-8">KEY-001</TableCell>
              <TableCell class="h-8">78</TableCell>
              <TableCell class="h-8 text-right">$79.99</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>

    <!-- Striped Table -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Striped Table</h2>
      <div class="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Order ID</TableHead>
              <TableHead>Customer</TableHead>
              <TableHead>Date</TableHead>
              <TableHead class="text-right">Total</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow class="odd:bg-muted/50">
              <TableCell class="font-medium">#ORD-001</TableCell>
              <TableCell>John Doe</TableCell>
              <TableCell>2024-01-15</TableCell>
              <TableCell class="text-right">$125.00</TableCell>
            </TableRow>
            <TableRow class="odd:bg-muted/50">
              <TableCell class="font-medium">#ORD-002</TableCell>
              <TableCell>Jane Smith</TableCell>
              <TableCell>2024-01-14</TableCell>
              <TableCell class="text-right">$89.50</TableCell>
            </TableRow>
            <TableRow class="odd:bg-muted/50">
              <TableCell class="font-medium">#ORD-003</TableCell>
              <TableCell>Bob Johnson</TableCell>
              <TableCell>2024-01-13</TableCell>
              <TableCell class="text-right">$203.75</TableCell>
            </TableRow>
            <TableRow class="odd:bg-muted/50">
              <TableCell class="font-medium">#ORD-004</TableCell>
              <TableCell>Alice Brown</TableCell>
              <TableCell>2024-01-12</TableCell>
              <TableCell class="text-right">$156.25</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>

    <!-- Empty State Table -->
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Empty State</h2>
      <div class="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Date</TableHead>
              <TableHead class="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell colspan="4" class="h-24 text-center">
                <div class="flex flex-col items-center gap-2">
                  <svg
                    class="h-8 w-8 text-muted-foreground"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                  <p class="text-muted-foreground">No data available</p>
                </div>
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>
  </div>
</template>
