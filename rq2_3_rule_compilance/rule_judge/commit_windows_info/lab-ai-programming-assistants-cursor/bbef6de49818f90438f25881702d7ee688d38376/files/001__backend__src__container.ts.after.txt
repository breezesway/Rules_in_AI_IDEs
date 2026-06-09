import { container } from "tsyringe";
import { DeepSeekServiceSingleton } from "./services/deepseek.service";
import type { IDeepSeekService } from "./services/deepseek.service";
import { PromptControllerSingleton } from "./controllers/prompt.controller";
import type { IPromptController } from "./controllers/prompt.controller";

// Register the dependencies - only register here, remove from individual service files
container.registerSingleton<IDeepSeekService>("IDeepSeekService", DeepSeekServiceSingleton);
container.registerSingleton<IPromptController>("IPromptController", PromptControllerSingleton);

export { container }; 