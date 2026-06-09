import { Outlet, createRootRoute } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools';

import { GNB } from '@/widgets/gnb';

export const Route = createRootRoute({
  component: RootComponent,
});

function RootComponent() {
  return (
    <div className="flex h-screen w-screen flex-col items-center justify-center">
      <div className="container mx-auto w-full flex-1">
        <div className="mt-10 flex flex-col items-center justify-center md:mx-20 lg:mx-40">
          <GNB />
          <div className="mt-10 w-full p-10">
            <Outlet />
          </div>
        </div>
        <TanStackRouterDevtools />
      </div>
    </div>
  );
}
