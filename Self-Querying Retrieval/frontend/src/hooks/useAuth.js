import { useMsal, useIsAuthenticated } from '@azure/msal-react';
import { useEffect, useState } from 'react';
import { InteractionRequiredAuthError } from '@azure/msal-browser';

const useAuth = () => {
    const { instance, accounts, inProgress } = useMsal();
    const isAuthenticated = useIsAuthenticated();
    const [token, setToken] = useState(null);

    useEffect(() => {
        const authenticateAndCheckRoles = async () => {
            if (!isAuthenticated && inProgress === 'none') {
                await instance.loginRedirect();
            }

            if (isAuthenticated) {
                try {
                    const account = accounts[0];
                    const response = await instance.acquireTokenSilent({
                        scopes: ["1c8a24dc-eda8-49a6-9e82-c40aea8ea822/.default"],
                        account: account
                    });
                    setToken(response.accessToken);

                } catch (error) {
                    if (error instanceof InteractionRequiredAuthError) {
                        // Trigger interactive login because silent token acquisition failed
                        instance.loginRedirect();
                    }
                    // Handle other errors (network failure, server down, etc.)
                }
            }
        };

        authenticateAndCheckRoles();
    }, [isAuthenticated, inProgress, instance, accounts]);

    return { isAuthenticated, user: accounts[0], token };
};

export default useAuth;